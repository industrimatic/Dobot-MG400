import dobot_api


class MG400_api:
    def __init__(self, ip: str = "192.168.1.6") -> None:
        self.dashboard = dobot_api.DobotApiDashboard(ip, 29999)
        self.move = dobot_api.DobotApiMove(ip, 30003)

    # ---------------- 开关 ----------------

    def enable(self, speed_ratio: int = 30) -> None:
        """使能机器人（松抱闸上电），并设置全局速度比例（1~100）。"""
        self.dashboard.EnableRobot()
        self.dashboard.SpeedFactor(speed_ratio)

    def close(self) -> None:
        """断开控制口和运动口。"""
        self.dashboard.close()
        self.move.close()

    # ---------------- 读位置 ----------------

    def get_pos(self) -> list:
        """读末端位姿 [x, y, z, r]，单位 mm / 度。"""
        # replay 长这样：'0,{284.458592,1.639760,115.044479,0.330278},GetPose();'
        replay = self.dashboard.GetPose()

        start = replay.index("{") + 1
        end = replay.index("}")
        context = replay[start:end]

        return [float(val) for val in context.split(",")]

    def get_angles(self) -> list:
        """读四个关节角 [j1, j2, j3, j4]，单位度。"""
        # replay 长这样：'0,{284.458592,1.639760,115.044479,0.330278},GetPose();'
        replay = self.dashboard.GetAngle()

        start = replay.index("{") + 1
        end = replay.index("}")
        context = replay[start:end]

        return [float(val) for val in context.split(",")]

    # ---------------- 移动 ----------------

    def move_to_point(
        self, x: float, y: float, z: float, r: float | None = None
    ) -> None:
        """让末端移动到 [x, y, z]（mm），阻塞到到位为止。

        走 MovJ：关节空间插值，最快，轨迹是弧线。
        想走直线请用 move_to_point_straight()。
        传 [x, y, z] 时保持当前末端角度 r；传 [x, y, z, r] 可同时改角度。
        """
        if r is None:
            r = self.get_pos()[3]
        self.move.MovJ(x, y, z, r)
        self.move.Sync()

    def move_to_point_straight(
        self, x: float, y: float, z: float, r: float | None = None
    ) -> None:
        """让末端沿直线移动到 [x, y, z]（mm），阻塞到到位为止。

        走 MovL：慢，但路径可预期，适合接近/离开工件。
        """
        if r is None:
            r = self.get_pos()[3]
        self.move.MovL(x, y, z, r)
        self.move.Sync()

    def move_by_angles(self, j1: float, j2: float, j3: float, j4: float) -> None:
        """让四个关节转到指定角度（度），并阻塞到到位为止。"""
        self.move.JointMovJ(j1, j2, j3, j4)
        self.move.Sync()

    def reset_pos(self) -> None:
        """回到零位：四个关节角全部归零。"""
        self.move_by_angles(0, 0, 0, 0)


if __name__ == "__main__":
    arm = MG400_api()
    arm.enable()
    print("当前位姿:", arm.get_pos())
    print("当前关节:", arm.get_angles())
    arm.close()
