"""Simple Ball Push After Detection"""

from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

camera = robot.getDevice("camera")
camera.enable(timestep)

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

width = camera.getWidth()
height = camera.getHeight()

# --- Push timer ---
push_steps = 0

def is_orange(r, g, b):
    return r > 120 and g > 60 and b < 150

while robot.step(timestep) != -1:

    image = camera.getImage()

    ball_count = 0
    ball_x_sum = 0

    # --- Scan image ---
    for x in range(0, width, 3):
        for y in range(0, height, 3):

            r = camera.imageGetRed(image, width, x, y)
            g = camera.imageGetGreen(image, width, x, y)
            b = camera.imageGetBlue(image, width, x, y)

            if is_orange(r, g, b):
                ball_count += 1
                ball_x_sum += x

    # --- If currently pushing → continue ---
    if push_steps > 0:
        left_motor.setVelocity(6)
        right_motor.setVelocity(6)
        push_steps -= 1
        continue

    # --- Ball detected ---
    if ball_count > 30:

        ball_x = ball_x_sum / ball_count

        # --- Align with ball ---
        if ball_x < width / 3:
            left_motor.setVelocity(2)
            right_motor.setVelocity(5)

        elif ball_x > 2 * width / 3:
            left_motor.setVelocity(5)
            right_motor.setVelocity(2)

        else:
            # 🔥 BALL CENTERED → START PUSH
            print("PUSHING BALL")

            push_steps = 10   # push for a few steps
            left_motor.setVelocity(6)
            right_motor.setVelocity(6)

    else:
        # --- Search ---
        left_motor.setVelocity(2)
        right_motor.setVelocity(-2)
