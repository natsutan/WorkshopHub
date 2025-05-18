import os
#os.environ['PYOPENGL_PLATFORM'] = 'glx'

import genesis as gs
import numpy as np
import socket
import json


# WSL2 マシン(またはサーバー側)のIPアドレスとポートを合わせる
# >wsl -- ip addr で確認できる
HOST = 'xxx.xx.xx.xxx'  # localhostで試す場合、WSL2/Windows間の通信は別IPになることも
PORT = 50007

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3, -1, 1.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=30,
        max_FPS=60,
    ),
    sim_options=gs.options.SimOptions(
        dt=0.01,
    ),
    show_viewer=True,
    rigid_options=gs.options.RigidOptions(
        box_box_detection=True,
    ),
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)
cube = scene.add_entity(
    gs.morphs.Box(
        size=(0.04, 0.04, 0.04),
        pos=(0.65, 0.0, 0.02),

    )
)
ur = scene.add_entity(
    gs.morphs.MJCF(file='D:/home/myproj/genesis/pybullet_ur5_gripper/robots/xml/ur5e.xml'),
    vis_mode='collision'
)

cam = scene.add_camera(
    res=(640, 480),
    pos=(3, -1, 1.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=False
)

finger_qpos = [0.04, 0.04, 0.04, 0.04, 0.04, 0.04]

def gripper_open():
    global finger_qpos
    finger_qpos = [-0.30, -0.30, -0.30, -0.30, 0.04, 0.04]

def gripper_close():
    global finger_qpos
    finger_qpos = [0.55, 0.55, 0.40, 0.40, 0.05, 0.05]


def ompl_waypoints(start, goal, num_waypoint):
    start_list = [float(x) for x in start]
    goal_list = [float(x) for x in goal]

    # 送信したいデータ
    data_to_send = {
        "qpos_start": start_list,
        "qpos_goal":  goal_list,
        "num_waypoint": num_waypoint
    }

    # ソケットを作ってサーバーに接続
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to server {HOST}:{PORT} ...")
        s.connect((HOST, PORT))

        # JSONでエンコードして送信
        message = json.dumps(data_to_send).encode()
        s.sendall(message)

        # レスポンス受信

        # JSONデコードして結果を表示
        response_data = recv_all(s)
        response = json.loads(response_data.decode())
        print("Received:", response)
        return response.get("waypoint")


def recv_all(sock):
    """ サーバーが送信を完了 or ソケット閉じるまで、繰り返し受信する """
    buffers = []
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            # サーバー側が close した
            break
        buffers.append(chunk)
    return b"".join(buffers)

########################## build ##########################
scene.build()

motors_dof = np.arange(6)
fingers_dof = np.arange(6, 12)
first_qpos = np.array([  -0, -0.9,  -0.5,  -1.4,  -1.3,  -0.3, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04])

# from franka_cube.py
kp = np.array([4500, 4500, 3500, 3500, 2000, 2000, 100, 100, 100, 100, 100, 100,])
kv = np.array([450,   450,  350,  350,  200,  200, 10, 10, 10, 10, 10, 10])


ur.set_dofs_kp(
    kp = kp,
)

ur.set_dofs_kv(
    kv = kv,
)

ur.set_qpos(first_qpos)
scene.step()


gripper_open()
for i in range(100):
    ur.control_dofs_position(first_qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

gripper_close()
for i in range(50):
    ur.control_dofs_position(first_qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

gripper_open()
for i in range(50):
    ur.control_dofs_position(first_qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()


end_effector = ur.get_link("tool0")

# workの真上に移動
start_qpos = first_qpos
goal_qpos = ur.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.40]),
    quat=np.array([0, 1, 0, 0]),
    dofs_idx_local = motors_dof
)
goal_qpos = list(goal_qpos)
goal_qpos[6:12] = finger_qpos
waypoints  = ompl_waypoints(start_qpos, goal_qpos, 200)

for qpos in waypoints:
    ur.control_dofs_position(qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

# EEを下げる
start_qpos = goal_qpos
goal_qpos = ur.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.15]),
    quat=np.array([0, 1, 0, 0]),
    dofs_idx_local = motors_dof
)
goal_qpos = list(goal_qpos)
goal_qpos[6:12] = finger_qpos
waypoints  = ompl_waypoints(start_qpos, goal_qpos, 100)
for qpos in waypoints:
    ur.control_dofs_position(qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

# grasp
gripper_close()
for i in range(100):
    ur.control_dofs_position(goal_qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

# lift
start_qpos = goal_qpos
goal_qpos = ur.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.3]),
    quat=np.array([0, 1, 0, 0]),
    dofs_idx_local = motors_dof
)

goal_qpos = list(goal_qpos)
goal_qpos[6:12] = finger_qpos
waypoints  = ompl_waypoints(start_qpos, goal_qpos, 100)

for qpos in waypoints:
    ur.control_dofs_position(qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()

# to the first position
start_qpos = goal_qpos
goal_qpos[6:12] = finger_qpos
waypoints  = ompl_waypoints(start_qpos, first_qpos, 200)
for qpos in waypoints:
    ur.control_dofs_position(qpos[0:6], motors_dof)
    ur.control_dofs_position(finger_qpos, fingers_dof)
    scene.step()