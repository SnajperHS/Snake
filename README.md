# Snake
Game Setup
Imports and Initialization:

The game imports several modules: Screen and Turtle from the turtle library, as well as time, and custom classes Snake, Food, and Scoreboard.
A Screen object is created to set up the game window.
Screen Configuration:

The screen is set to be 600x600 pixels, with a black background and a title "Snake Game".
screen.tracer(0) is used to turn off automatic screen updates, which allows manual control for smoother animation using screen.update().
Game Objects:

Snake: An instance of the Snake class is created, representing the snake that the player controls.
Food: An instance of the Food class is created, representing the food that the snake needs to eat to grow.
Scoreboard: An instance of the Scoreboard class is created to keep track of and display the player's score.
Game Mechanics
Snake Movement:

The snake is controlled using arrow keys. The player can change the snake's direction by pressing "Up", "Down", "Left", or "Right".
The Snake class handles the movement and growth of the snake, ensuring that the snake moves in the direction specified by the player.
Game Loop:

The game runs a loop controlled by the game_is_on boolean variable.
Inside the loop, the screen updates every 0.1 seconds to create the effect of animation.
The snake moves forward continuously unless the player changes its direction.
Food Collection:

The snake can collect food by coming within a certain distance (15 pixels) of the food object.
When the snake collects food, the Food object is refreshed (moved to a new random location), and the snake grows by one segment using the extend() method.
The scoreboard updates to reflect the new score.
Collision Detection:

The game checks for collisions with the screen's edges. If the snake's head moves beyond the screen boundaries (x or y coordinate greater than ±280), the snake resets, and the score is updated.
The game also checks for collisions with the snake's own tail. If the head comes within 10 pixels of any of its segments, the snake resets.
Score Management:

The Scoreboard class manages the score. If the player beats the high score, it is updated and stored in data.txt.
When the game resets, the score is set to zero, and the scoreboard displays the current and high scores.
Class Breakdown
Snake Class
Attributes: Handles the creation and management of the snake's segments.
Methods:
create_snake(): Initializes the snake with a default size.
move(): Moves each segment of the snake forward.
extend(): Adds a new segment to the snake when food is eaten.
reset(): Resets the snake's position and size when a collision occurs.
Directional methods (up, down, left, right) handle changes in the snake's heading.
Scoreboard Class
Attributes: Manages and displays the current score and high score.
Methods:
update_scoreboard(): Updates the scoreboard display with the current score.
reset(): Resets the score and updates the high score if needed.
increase_score(): Increments the score when food is eaten and updates the display.
