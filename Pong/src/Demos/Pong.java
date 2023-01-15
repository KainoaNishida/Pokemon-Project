package Demos;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.KeyEvent;
import java.util.Random;

import Utilities.GDV5;

public class Pong extends GDV5 {
	
	Ball r1 = new Ball(380, 300);
	Ball demoBall = new Ball(510, 100);
	Paddle lpaddle = new Paddle(0, 250);
	Paddle rpaddle = new Paddle(785, 250);
	Paddle demoLeftPaddle = new Paddle(350, 60);
	Paddle demoRightPaddle = new Paddle(700, 60);
	
	Rectangle color1 = new Rectangle(50, 50, 35, 35);
	Rectangle color2 = new Rectangle(50, 100, 35, 35);
	Rectangle color3 = new Rectangle(50, 150, 35, 35);
	Rectangle color4 = new Rectangle(50, 200, 35, 35);
	Rectangle color5 = new Rectangle(50, 250, 35, 35);
	Rectangle color6 = new Rectangle(50, 300, 35, 35);
	Rectangle color7 = new Rectangle(50, 350, 35, 35);
	
	int maxPoints; //create a option for people to change the winning score. when it is reached, display name of victor
	
	boolean red; //these are the color options for the paddle if you are playing single player
	boolean orange;
	boolean yellow;
	boolean green;
	boolean blue;
	boolean magenta;
	boolean white;
	boolean isResetting = false;
	
	int speed = 3; //the initial speed of every game is 6
	int a = randomDirection();
	int b = randomDirection();
	
	int fps = 60; //allows the game to reset
	int pauseTimeInSeconds =  2;
	int resetFrames = fps * pauseTimeInSeconds;
	int resetCounter = 0;
	
	Color c1 = Color.WHITE; //sets the color of the ball to white
	
	boolean titleScreen = true; //these are all of the different screens
	boolean singlePlayer1;
	boolean singlePlayer2;
	boolean doublePlayer1;
	boolean doublePlayer2;
	boolean victoryScreen;
	boolean player1Victory;
	boolean player2Victory;

	int five = 1; //five is an algorithm that increases the speed by 1 (in single player) if the ball collides with the paddles 5 times.
	int two = 2;
	
	Point center = new Point(380, 300); //the center of the screen for the ball
	
	int ldy = 0;
	int rdy = 0;
	int demoMovement = 5;
	double cpuSpeed = 9.0; //the speed of the opponent in single player
	
	int lpoints = 0;
	int rpoints = 0;

	
	public void reset() {
		this.isResetting = true;
		this.resetCounter = this.resetFrames;
		lpaddle.resetLocation();
		rpaddle.resetLocation();
	}
	
	public void changeColor() {
		Color c1 = new Color((float) Math.random(), (float) Math.random(), (float) Math.random());
		this.c1 = c1;
	}
	
	public int randomDirection() { //gives a random direction for both horizontal and vertical movement of the ball
		int positive = speed;
		int negative = -speed;
		
		Random random = new Random();
		
		int randomOfTwoInts = random.nextBoolean() ? positive : negative;
		return randomOfTwoInts;
	}

	public void resetSpeed(int newSpeed) {
		this.speed = newSpeed;
		this.a = randomDirection();
		this.b = randomDirection();
	}
	
	public void move() { //moves the ball using the translate method
		r1.translate(this.a, this.b);
	}
	
	public void randomMovement() { //gives a random movement to the ball by using random values from the randomDirection() method
		this.a = randomDirection();
		this.b = randomDirection();
	}
	
	public void update() {//updates 60 times per second		
		
		if ((rpoints == 5)) {
			victoryScreen = true;
			player2Victory = true;
			singlePlayer2 = false;
			doublePlayer2 = false;
			player1Victory = false;
			lpoints = 0;
			rpoints = 0;
		}
		
		if ((lpoints == 5)) {
			victoryScreen = true;
			player2Victory = false;
			singlePlayer2 = false;
			doublePlayer2 = false;
			player1Victory = true;
			lpoints = 0;
			rpoints = 0;
		}
		
		if (singlePlayer1 == true) {
			demoBall.translate(demoMovement,  0);
			
			if (demoBall.intersects(demoRightPaddle)) {
				demoMovement = -5;
			}
			
			if (demoBall.intersects(demoLeftPaddle)) {
				demoMovement = 5;
			}
		}
		
		if (singlePlayer2 == true) { //when singlePlayer2 is true, the single player game has begun
				
				if (this.isResetting == false) {
					if ((two % 2) == 0) {
						speed = 3;
						two++;
					}
					
					r1.translate(this.a,  this.b); //moves ball
					
					if ((five % 5) == 0) { //every 4 hits, the speed increases by 1
						speed++;
						five++;
					}
					
					lpaddle.translate(0, ldy); //moves left paddle when a specific key is pressed
					rpaddle.translate(0, rdy);
				
					if (r1.getX() <= 0) { //resets the game and adds points when the ball gets past the left paddle
						rpoints++;
						r1.setLocation(center);
						two++;
						reset();
					}
				
					if (r1.getX() >= 775) { //resets the game and adds points when the ball gets past the right paddle
						lpoints++;
						r1.setLocation(center);
						two++;
						reset();
						
					}
				
					if (r1.getY() >= 575) { //changes direction of ball if it hits the top of the screen
						this.b = -Math.abs(speed);
					}
				
					if (r1.getY() <= 0) {  //changes direction of ball if it hits the bottom of the screen
						this.b = Math.abs(speed);
					}
				
					if (r1.intersects(lpaddle) == true) {  //changes direction of ball if it hits the left paddle
						five++;
						this.a = Math.abs(speed);
					}
				
					if (r1.intersects(rpaddle) == true) { //changes direction of ball if it hits the right paddle
						five++;
						this.a = -Math.abs(speed);
					}
					
					if (rpaddle.getY() < r1.getY()) { //moves the cpu by comparing its y values with the y values of the ball
						rdy = (int) cpuSpeed;
					}
					
					if (rpaddle.getY() > r1.getY()) { //moves the cpu by comparing its y values with the y values of the ball
						rdy = - (int) cpuSpeed;
					}
					
					if (lpoints == 10) {
						singlePlayer2 = false;
						victoryScreen = true;
						player1Victory = true;
					}
					
					if (rpoints == 10) {
						singlePlayer2 = false;
						victoryScreen = true;
						player2Victory = true;
					}
					
				} else {
					
					if (this.resetCounter <= 1) {
						this.isResetting = false;
						resetSpeed(3);
					}
					this.resetCounter -= 1;
				}
		}
		
		if (doublePlayer2 == true) {
			if (this.isResetting == false) {
				r1.translate(this.a, this.b);

				lpaddle.translate(0, ldy);
				rpaddle.translate(0, rdy);


				if (speed > 10) {
					speed = 10;
				}

				if (r1.getX() <= 0) {
					rpoints++;
					r1.setLocation(center);
					reset();
				}

				if (r1.getX() >= 775) {
					lpoints++;
					r1.setLocation(center);
					reset();
				}

				if (r1.getY() >= 575) {
					this.b = -Math.abs(speed);
				}

				if (r1.getY() <= 0) {
					this.b = Math.abs(speed);
				}

				if ((r1.intersects(lpaddle) == true) && (ldy != 0)) {
					speed++;
					this.a = Math.abs(speed);
				}

				if ((r1.intersects(lpaddle) == true) && (ldy == 0)) {
					speed = 4;
					this.a = Math.abs(speed);
				}

				if ((r1.intersects(rpaddle) == true) && (rdy != 0)) {
					speed++;
					this.a = -Math.abs(speed);
				}

				if ((r1.intersects(rpaddle) == true) && (rdy == 0)) {
					speed = 4;
					this.a = -Math.abs(speed);
				}
				
				if (lpoints == 10) {
					singlePlayer2 = false;
					victoryScreen = true;
					player1Victory = true;
				}
				
				if (rpoints == 10) {
					singlePlayer2 = false;
					victoryScreen = true;
					player2Victory = true;
				}
				
			} else {

				if (this.resetCounter <= 1) {
					this.isResetting = false;
					resetSpeed(3);
				}
				this.resetCounter -= 1;
			}
		}
	}
	
	@Override
	public void keyPressed(KeyEvent e) {
		KeysPressed[e.getKeyCode()] = true;
		
		if ((titleScreen == true) && (e.getKeyCode() == 50)) {
				doublePlayer1 = true;
				titleScreen = false;
		}
		
		if ((titleScreen == true) && (e.getKeyCode() == 49)) {
			singlePlayer1 = true;
			titleScreen = false;
		}
		
		if ((singlePlayer1 == true) && (e.getKeyCode() ==32)) {
			singlePlayer2 = true;
			singlePlayer1 = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true)) && e.getKeyCode() == 82) {
			red = true;
			orange = false;
			yellow = false;
			green = false;
			blue = false;
			magenta = false;
			white = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true)) && e.getKeyCode() == 79) {
			red = false;
			orange = true;
			yellow = false;
			green = false;
			blue = false;
			magenta = false;
			white = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true))  && e.getKeyCode() == 89) {
			red = false;
			orange = false;
			yellow = true;
			green = false;
			blue = false;
			magenta = false;
			white = false;
		}

		if (((singlePlayer1 == true) || (singlePlayer2 == true)) && e.getKeyCode() == 71) {
			red = false;
			orange = false;
			yellow = false;
			green = true;
			blue = false;
			magenta = false;
			white = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true))  && e.getKeyCode() == 66) {
			red = false;
			orange = false;
			yellow = false;
			green = false;
			blue = true;
			magenta = false;
			white = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true)) && e.getKeyCode() == 80) {
			red = false;
			orange = false;
			yellow = false;
			green = false;
			blue = false;
			magenta = true;
			white = false;
		}
		
		if (((singlePlayer1 == true) || (singlePlayer2 == true)) && e.getKeyCode() == 68) {
			red = false;
			orange = false;
			yellow = false;
			green = false;
			blue = false;
			magenta = false;
			white = true;
		}
		
		if ((singlePlayer1 == true) && e.getKeyCode() == 32) {
			singlePlayer2 = true;
			singlePlayer1 = false;
		}
		
		if ((doublePlayer1 == true) && (e.getKeyCode() == 32)) {
			doublePlayer2 = true;
			doublePlayer1 = false;
		}
			
		if (doublePlayer2 == true || singlePlayer2 == true) {
			
			if (e.getKeyCode() == 87) {
				ldy = -6;
			}

			if (e.getKeyCode() == 83) {
				ldy = 6;
			}
		}
		
		if (doublePlayer2 == true) {
			if (e.getKeyCode() == 38) {
				rdy = -6;
			}
			
			if (e.getKeyCode() == 40) {
				rdy = 6;
			}
		}
	}
	
	@Override
	public void keyReleased(KeyEvent e) {
		
		if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE) {
			titleScreen = true;
			singlePlayer1 = false;
			singlePlayer2 = false;
			doublePlayer1 = false;
			doublePlayer2 = false;
			victoryScreen = false;
			player1Victory = false;
			player2Victory = false;
		}
		
		if (doublePlayer2 == true || singlePlayer2 == true) {
			KeysPressed[e.getKeyCode()] = false;
			KeysTyped[e.getKeyCode()] = true;
		
			if (e.getKeyCode() == 38 || e.getKeyCode() == 40) {
				rdy = 0; //problem because it shuts off both, but we only want one to shut off
			}
		
			if (e.getKeyCode() == 83 || e.getKeyCode() == 87 ) {
				ldy = 0;
			}
		}
	}
	
	@Override
	public void keyTyped(KeyEvent e) {
		
	}
	
	public void draw(Graphics2D win) {
		
		if ((victoryScreen == true) && (player1Victory == true)) {
			win.setColor(Color.WHITE);
			
			Font font = new Font("Synchro LET", Font.PLAIN, 60);
			win.setFont(font);
			win.drawString("Player 1 is the Winner!", 100, 300);
			
			Font escapeOption = new Font("Synchro LET", Font.PLAIN, 15);
			win.setFont(escapeOption);
			win.drawString("Press delete to return to the main menu.", 490, 590);
		}
		
		if ((victoryScreen == true) && (player2Victory == true)) {
			win.setColor(Color.WHITE);
			
			Font font = new Font("Synchro LET", Font.PLAIN, 60);
			win.setFont(font);
			win.drawString("Player 2 is the Winner!", 100, 300);
			
			Font escapeOption = new Font("Synchro LET", Font.PLAIN, 15);
			win.setFont(escapeOption);
			win.drawString("Press delete to return to the main menu.", 245, 590);
		}
		
		if (titleScreen == true) {
			
		win.setColor(Color.WHITE);
		
		Font title = new Font("STHeiti", Font.BOLD, 110);
		win.setFont(title);
		win.drawString("PONG", 240, 320);
		
		Font subtitle = new Font("Synchro LET", Font.PLAIN, 20);
		win.setFont(subtitle);
		win.drawString("Press 1 for single player", 290, 450);
		win.drawString("Press 2 for double player", 290, 480);
		
		Font escapeOption = new Font("Synchro LET", Font.PLAIN, 15);
		win.setFont(escapeOption);
		win.drawString("Press delete at any time to return to the main menu.", 230, 590);
		}
		
		else if (singlePlayer1 == true) {
			
			win.setColor(Color.WHITE);
			
			Font tutorial = new Font("Synchro LET", Font.PLAIN, 30);
			win.setFont(tutorial);
			win.drawString("TUTORIAL", 460, 240);
					
			Font firstTo5Points = new Font("Synchro LET", Font.PLAIN, 25);
			win.setFont(firstTo5Points);
			win.drawString("First to 5 points wins", 420 , 375);
			
			Font enter = new Font("Synchro LET", Font.PLAIN, 20);
			win.setFont(enter);
			win.drawString("Press Space to play", 440, 500);
			win.drawString("w ", 470, 290);
			win.drawString("s   ", 472, 330);
			
			win.drawString("move up", 510, 290);
			win.drawString("move down", 510, 330);
			
			win.setColor(Color.WHITE);
			Font font = new Font("Synchro LET", Font.PLAIN, 15);
			win.setFont(font);
			win.drawString("press r for red", 100, 70);
			win.drawString("press o for orange", 100, 120);
			win.drawString("press y for yellow", 100, 170);
			win.drawString("press g for green", 100, 220);
			win.drawString("press b for blue", 100, 270);
			win.drawString("press p for purple", 100, 320);
			win.drawString("press d for default (white)", 100, 370);
			
			win.drawRect(461, 267, 30, 30);
			win.drawRect(461, 307, 30, 30);
			win.drawRect(382, 200, 300, 200);
			
			win.fill(demoBall);
			win.fill(demoRightPaddle);
			win.fill(demoLeftPaddle);
			
			win.setColor(Color.RED);
			win.fill(color1);
			
			win.setColor(Color.ORANGE);
			win.fill(color2);
			
			win.setColor(Color.YELLOW);
			win.fill(color3);
			
			win.setColor(Color.GREEN);
			win.fill(color4);
			
			win.setColor(Color.BLUE);
			win.fill(color5);
			
			win.setColor(Color.MAGENTA);
			win.fill(color6);
			
			win.setColor(Color.WHITE);
			win.fill(color7);
			
			if (red == true) {
				win.setColor(Color.RED);
				win.fill(demoLeftPaddle);
			}
			
			if (orange == true) {
				win.setColor(Color.ORANGE);
				win.fill(demoLeftPaddle);
			}
			
			if (yellow == true) {
				win.setColor(Color.YELLOW);
				win.fill(demoLeftPaddle);
			}
			
			if (green == true) {
				win.setColor(Color.GREEN);
				win.fill(demoLeftPaddle);
			}
			
			if (blue == true) {
				win.setColor(Color.BLUE);
				win.fill(demoLeftPaddle);
			}
			
			if (magenta == true) {
				win.setColor(Color.MAGENTA);
				win.fill(demoLeftPaddle);
			}
			
			if (white == true) {
				win.setColor(Color.WHITE);
				win.fill(demoLeftPaddle);
			}
		}
		
		else if (singlePlayer2 == true) {
			
			Font font = new Font("Synchro LET", Font.PLAIN, 35);
			win.setFont(font);
			win.setColor(Color.WHITE);
			win.drawString(Integer.toString(lpoints), 50, 100);
			win.drawString(Integer.toString(rpoints), 710, 100);
			
			Font playerName = new Font("Synchro LET", Font.PLAIN, 20);
			win.setFont(playerName);
			win.drawString("Player 1", 25, 50);
			win.drawString("Player 2", 680, 50);
			
			win.setColor(this.c1);
			win.fill(r1);
			
			win.setColor(Color.WHITE);
			win.fill(rpaddle);
			win.fill(lpaddle);
			
			if (red == true) {
				win.setColor(Color.RED);
				win.fill(lpaddle);
			}
			
			if (orange == true) {
				win.setColor(Color.ORANGE);
				win.fill(lpaddle);
			}
			
			if (yellow == true) {
				win.setColor(Color.YELLOW);
				win.fill(lpaddle);
			}
			
			if (green == true) {
				win.setColor(Color.GREEN);
				win.fill(lpaddle);
			}
			
			if (blue == true) {
				win.setColor(Color.BLUE);
				win.fill(lpaddle);
			}
			
			if (magenta == true) {
				win.setColor(Color.MAGENTA);
				win.fill(lpaddle);
			}
			
			if (white == true) {
				win.setColor(Color.WHITE);
				win.fill(lpaddle);
			}
			
		}
		
		else if (doublePlayer1 == true) {
			win.setColor(Color.WHITE);
			
			Font enter = new Font("Synchro LET", Font.PLAIN, 20);
			win.setFont(enter);
			win.drawString("Press Space to play", 560, 530);
			
			win.drawString("To increase the ball's speed, move your paddle while striking the ball.", 100, 100);
			win.drawString("To reset the ball's speed, keep your paddle still while striking the ball.", 100, 130);
			win.drawString("First to 5 points wins", 310, 160);
			
			win.drawString(" Player1", 100, 300);
			win.drawString("Move up", 150, 355);
			win.drawString("Move up", 150, 405);
			win.drawString("w", 68, 353);
			win.drawString("s", 70, 403);
			win.drawString("-", 120, 353);
			win.drawString("-", 120, 403);
			
			
			win.drawRect(60, 330, 30, 30);
			win.drawRect(60, 380, 30, 30);
			win.drawRect(50, 50, 700, 150);
			win.drawRect(45, 250, 200, 200);
			win.drawRect(475, 250, 300, 200);
			
			
			
			win.drawString("Player2", 590, 300);
			win.drawString("Move up", 640, 355);
			win.drawString("Move down", 640, 405);
			win.drawString("   Up arrow    -", 500, 353);
			win.drawString("Down arrow   -", 498, 403);
		}
		
		else if (doublePlayer2 == true)  {
			win.setColor(this.c1);
			win.fill(r1);
			
			win.setColor(Color.white);
			win.fill(lpaddle);
			
			win.setColor(Color.white);
			win.fill(rpaddle);
		
			Font font = new Font("Synchro LET", Font.PLAIN, 35);
			win.setFont(font);
			win.drawString(Integer.toString(lpoints), 50, 100);
			win.drawString(Integer.toString(rpoints), 710, 100);
			
			Font playerName = new Font("Synchro LET", Font.PLAIN, 20);
			win.setFont(playerName);
			win.drawString("Player 1", 25, 50);
			win.drawString("Player 2", 680, 50);
		}
		
	}
	
	public static void main(String[] args) {
		Pong game = new Pong();
		game.start();
	}
}



