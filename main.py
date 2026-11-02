from MG400 import MG400_api
import time
import manyterm

t1 = manyterm.Terminal()
arm = MG400_api()
arm.enable()
arm.reset_pos()

for i in range(1):
    arm.move_by_angles(30, 0, 0, 0)
    t1.print(f"[info] Now Pos: {arm.get_pos()}")
    t1.print(f"[info] Now Angles: {arm.get_angles()}")
    time.sleep(0.5)
    arm.move_by_angles(-30, 0, 0, 0)
    t1.print(f"[info] Now Pos: {arm.get_pos()}")
    t1.print(f"[info] Now Angles: {arm.get_angles()}")
    time.sleep(0.5)

arm.reset_pos()
arm.close()
