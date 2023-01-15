
package Battleship;

abstract class Boat {
	private int team;
	private Coordinates location;
	private int direction;
	private int health;
	private int strength;
	private int vision;

	public Boat(int team, Coordinates location, int direction, int health, int strength, int vision) {
		this.team = team;
		this.location = location;
		this.direction = direction;
		this.health = health;
		this.strength = strength;
		this.vision = vision;
	}
	
	public int getTeam() {
		return this.team;
	}

	public Coordinates getLocation() {
		return this.location;
	}
	
	public int getDirectionNum() {
		return this.direction;
	}
	
	public char getDirection() {
		if(direction == 0) {
			return '\u2191';
		}
		if(direction == 1) {
			return '\u2197';
		}
		if(direction == 2) { 
			return '\u2192';
		}
		if(direction == 3) {
			return '\u2198';
		}
		if(direction == 4) {
			return '\u2193';
		}
		if(direction == 5) {
			return '\u2199';
		}
		if(direction == 6) {
			return '\u2190';
		}
		if(direction == 7) {
			return '\u2196';
		}
		return ' ';
	}
	
	public String getDirectionName(int direction) {
		if(direction == 0) {
			return "N";
		}
		if(direction == 1) {
			return "NE";
		}
		if(direction == 2) { 
			return "E";
		}
		if(direction == 3) {
			return "SE";
		}
		if(direction == 4) {
			return "S";
		}
		if(direction == 5) {
			return "SW";
		}
		if(direction == 6) {
			return "W";
		}
		if(direction == 7) {
			return "NW";
		}
		return "";
	}
	
	public int getHealth() {
		return this.health;
	}
	
	public int getStrength() {
		return this.strength;
	}
	
	public int getVision() {
		return this.vision;
	}
	
	
	abstract public String getID();
	
	abstract public String act(int[] userChoices, World world);
	
	abstract public String getActions();
	
	public String move(World world) {
		
		Coordinates location = this.getLocation();
		if(world.isLocationValid(world.getAdjacentLocation(location, direction))){
			Coordinates newLocation = world.getAdjacentLocation(location, direction);
			if(!world.isLocationOccupied(newLocation)){
				world.setOccupant(this, newLocation);
				world.setOccupant(null, location);
				return this.getID() + " moves from " + location.toString() + " to " + this.getLocation() + ".";
			}
			
			return this.toString() + " could not to " + newLocation.toString() + " as it is occupied.";
		}
		return this.toString() + " cannot move off the map.";
	}
	
	public String turn(int dir) {
		if (dir == 1) {
			if(direction < 7) {
				direction += 1;
			}
			if(direction == 7) {
				direction = 0;
			}
			return this.toString() + " turned right, now facing " + this.getDirectionName(direction);
		}
		if (dir == -1) {
			if(direction > 0) {
				direction -= 1;
			}
			else if(direction == 0) {
				direction = 7;
			}
			return this.toString() + " turned left, now facing " + this.getDirectionName(direction);
		}
		return "Input either -1 or 1.";
	}

	public void sink(World w) {
		w.setOccupant(null, this.getLocation());
	}
	
	public String takeHit(int attackStrength) {
		if (this.health - attackStrength >= 0) {
			this.health -= attackStrength;
		}
		else {
			this.health = 0;
		}
		if (this.health > 0) {
			return this.toString() + " takes " + attackStrength + " damage.";
		}
		return this.toString() + " has been sunk!";	
	}
	
	public void setLocation(Coordinates coordinates) {
		this.location = coordinates;
	}
	
	public String toString() {
		return this.getID();
	}
}
