from controller import Robot

# --- INITIAL SETUP ---
robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())
MAX_SPEED = 6.28

# --- CAMERA ---
cam = robot.getDevice("camera")
cam.enable(TIME_STEP)
width = cam.getWidth()
height = cam.getHeight()

# --- MOTORS ---
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

print("Robot started: searching for ball...")

# --- MAIN LOOP ---
while robot.step(TIME_STEP) != -1:

    image = cam.getImage()

    # IMPORTANT: check camera working
    if image is None:
        print("Camera not working")
        continue

    ball_pixels = []

    # --- IMPROVED COLOR DETECTION ---
    for x in range(0, width, 2):   # was 4 → now better detection
        for y in range(0, height, 2):

            r = cam.imageGetRed(image, width, x, y)
            g = cam.imageGetGreen(image, width, x, y)
            b = cam.imageGetBlue(image, width, x, y)

            # RELAXED ORANGE DETECTION (VERY IMPORTANT)
            if r > 80 and g > 40 and b < 120:
                ball_pixels.append(x)

    # --- DEBUG ---
    print("Detected pixels:", len(ball_pixels))

    # --- BEHAVIOUR ---
    if len(ball_pixels) > 20:   # ignore noise

        center_x = sum(ball_pixels) / len(ball_pixels)
        error = center_x - width / 2

        # --- CLOSE → PUSH ---
        if len(ball_pixels) > (width * height * 0.05):
            print("Pushing ball")
            left_speed = MAX_SPEED * 0.5
            right_speed = MAX_SPEED * 0.5

        else:
            # --- MOVE TOWARD BALL ---
            turn = 0.01 * error

            left_speed = MAX_SPEED * 0.6 - turn
            right_speed = MAX_SPEED * 0.6 + turn

            print("Tracking ball")

    else:
        # --- SEARCH ---
        print("Searching...")
        left_speed = 2.0
        right_speed = -2.0

    # --- LIMIT SPEED ---
    left_speed = max(min(left_speed, MAX_SPEED), -MAX_SPEED)
    right_speed = max(min(right_speed, MAX_SPEED), -MAX_SPEED)

    # --- APPLY ---
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)