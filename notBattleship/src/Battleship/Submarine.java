
package Battleship;

public class Submarine extends ScoutBoat implements Attacker{
	
	private int numOfTorpedoes;
	
	public Submarine(int team, Coordinates c, int dir, int numOfTorpedoes) {
		super(team, c, dir, 3, 2);
		this.numOfTorpedoes = numOfTorpedoes;
	}
	
	public String getID() {
		return "S" + this.getTeam();
	}
	
	public String getActions() {
		String s = "Choose any of the following actions for the Submarine:\n1. Move\n2. Turn left\n3. Turn right\n4. Submerge\n";
		if (this.numOfTorpedoes > 0) {
			s += "5. Fire torpedoes";
		}
		return s;
	}
	
	public String act(int[] choices, World w) {
		for(int choice: choices) {
			if(choice == 1) {
				return this.move(w);
			}
			if(choice == 2) {
				return this.turn(-1);
			}
			if (choice == 3) {
				return this.turn(1);
			}
			if (choice == 4) {
				return this.submerge(w);
			}
			if (choice == 5) {
				return this.attack(w);
			}
		}
		return null;
	}
	
	public String attack(World w) {
		int team = this.getTeam();
		int attackStrength;
		Coordinates location = w.getAdjacentLocation(this.getLocation(), this.getDirectionNum());
		
		if(numOfTorpedoes > 0) {
			for(int i=0; i < this.getVision(); i++) {
				if(w.isLocationValid(location))	{
					
					if(w.isLocationOccupied(location)) {

						if(w.getOccupant(location).getTeam() != team){
							
							attackStrength = (int)(Math.random()*w.getOccupant(location).getStrength()+1);
							numOfTorpedoes -= 1;
							return "Fire torpedoes! " + w.getOccupant(location).takeHit(attackStrength);
						}
					}
					location = w.getAdjacentLocation(location, this.getDirectionNum());
				}
				else {
					return "There are no boats in range currently.";
				}
			}
			return "There are no boats in range currently.";
		}
		return this.getID() + " has no torpedoes remaining.";
	}
	
	public String submerge(World w) {
		
		Coordinates location = this.getLocation();
		
		while (true) {

			Coordinates randomLocation = new Coordinates((int)(Math.random()*w.getWidth()), (int)(Math.random()*w.getHeight()));
			if(w.isLocationValid(randomLocation))	
				
				if(Math.abs(randomLocation.getX()-location.getX()) > 2 && Math.abs(randomLocation.getY()-this.getLocation().getY()) > 2 && !w.isLocationOccupied(randomLocation)){
					w.setOccupant(null, location);
					w.setOccupant(this, randomLocation);
					return this.getID() + " moves from " + location.toString() + " to " + randomLocation.toString();
	
				}
		}
	}
}
