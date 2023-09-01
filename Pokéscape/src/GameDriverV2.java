
/**
 * @(#)GameDriver.java
 *
 *
 * @author Mr. Gonzalez, Nicholas Hernandez
 * @version 2.0 6/2/2015
 */

import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Canvas;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

import javax.imageio.ImageIO;

public abstract class GameDriverV2 extends Canvas  {

	protected BufferedImage back;
	protected int FramesPerSecond = 60;
	protected long timer = 1000 / FramesPerSecond;
	protected Timer t1 = new Timer();
	
	public GameDriverV2() {
		// set up all variables related to the game

		// number of key possibilities
		
		
		setVisible(true);
		t1.scheduleAtFixedRate(new ThreadTimer(this), 0, timer);
		
		setFocusable(true);
	}

	public void update(Graphics window) {
		paint(window);
	}

	public void setTimer(int value) {
		timer = value;
	}

	public void paint(Graphics window) {
		if (back == null)
			back = (BufferedImage) (createImage(getWidth(), getHeight()));
		Graphics2D graphToBack = (Graphics2D) back.createGraphics();

		draw(graphToBack);

		Graphics2D win2D = (Graphics2D) window;
		win2D.drawImage(back, null, 0, 0);

	}

	public abstract void draw(Graphics2D win);

	
	private class ThreadTimer extends TimerTask {
		GameDriverV2 driver;

		public ThreadTimer(GameDriverV2 gameDrive) {
			driver = gameDrive;
		}

		@Override
		public void run() {
			driver.repaint();
			System.gc();
		}
	}
	public class timerDriver extends Thread{
		int delay;
		public timerDriver(int _delayInMiliseconds){
			delay= _delayInMiliseconds;
		}
		
		public void run(){
			
		}
		
		
	}
	
	public BufferedImage addImage(String name)  {

		BufferedImage img = null;
		try {
		
			img = ImageIO.read(this.getClass().getResource(name));
		
		} catch (IOException e) {
			System.out.println(e);
		}
		
		return img;

	}
	
}
