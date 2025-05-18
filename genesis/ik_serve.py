# server.py
import socket
import json

HOST = '0.0.0.0'  # どこからの接続でも受け付けたい場合は 0.0.0.0
PORT = 50007      # 適当なポート番号を指定


import os
#os.environ['PYOPENGL_PLATFORM'] = 'glx'

import genesis as gs
import numpy as np

########################## init ##########################
gs.init(backend=gs.cpu)

########################## create a scene ##########################
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.01,
    ),
    show_viewer=False,
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
    gs.morphs.MJCF(file='/home/natu/myproj/genesis/pybullet_ur5_gripper/robots/xml/ur5e.xml'),

    vis_mode='collision'
)

########################## build ##########################
scene.build()

motors_dof = np.arange(6)
fingers_dof = np.arange(6, 12)

# from franka_cube.py
kp = np.array([4500, 4500, 3500, 3500, 2000, 2000, 100, 100, 100, 100, 100, 100,])
kv = np.array([450,   450,  350,  350,  200,  200, 10, 10, 10, 10, 10, 10])

ur.set_dofs_kp(
    kp = kp,
)

ur.set_dofs_kv(
    kv = kv,
)


def handle_client(conn):
    """
    クライアントから1回分のリクエストを受け取り、waypoint を返す処理
    """
    try:
        # 1) データ受信
        data = conn.recv(4096)
        if not data:
            return

        # 2) JSONをパース
        received = json.loads(data.decode())
        qpos_start = received["qpos_start"]
        qpos_goal  = received["qpos_goal"]
        num_waypoint = received["num_waypoint"]

        # 3) サンプルとして、開始姿勢から目標姿勢を線形補間した waypoint を作る
        try:
            waypoints_tensor = ur.plan_path(
                qpos_start=qpos_start,
                qpos_goal=qpos_goal,
                num_waypoints=num_waypoint,  # 2s duration
                ignore_collision=True
            )
            waypoints = []
            for wp in waypoints_tensor:
                pose = []
                for p in wp:
                    pose.append(float(p))

                waypoints.append(pose)

        except Exception as e:
            print("[ERROR in generating waypoint]", e)
            waypoints = []

        # 4) JSONでレスポンスを作成して送信
        response = {"waypoint": waypoints}
        conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print("[ERROR in handle_client]", e)
    finally:
        conn.close()

def main():
    # ソケットを作って待ち受けを開始
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)  # 同時接続数(キュー)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print("Client connected:", addr)
            handle_client(conn)




if __name__ == "__main__":
    main()
