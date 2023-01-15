package Battleship;

public class Coordinates {
	
	private int x, y;
	
	public Coordinates(){
		this.x = 0;
		this.y = 0;
	}
	
	public Coordinates(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public int getX() {
		return this.x;
	}
	
	public int getY() {
		return this.y;
	}
	
	public void setCoordinates(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public String toString(){
		return (char)(y+65) + String.valueOf(x+1);
	}

}
