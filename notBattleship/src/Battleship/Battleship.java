
package Battleship;

public class Battleship extends Boat implements Attacker{

	public Battleship(int team, Coordinates c, int dir) {
		super(team, c, dir, 4, 3, 1);
	}
	
	public String getID() {
		return "B" + this.getTeam();
	}
	
	public String getActions() {
		return "Choose any of the following actions for the Aircraft Carrier:\n1. Move\n2. Turn left\n3. Turn right\n4. Attack";
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
				return this.attack(w);
			}
		}
		return null;
	}
	
	public String attack(World w) {
		int team = this.getTeam();
		Coordinates location = w.getAdjacentLocation(this.getLocation(), this.getDirectionNum());
		
		for(int i=0; i < this.getVision(); i++) {
			if(w.isLocationValid(location))	{
				if(w.isLocationOccupied(location)) {
					if(w.getOccupant(location).getTeam() != team){
						return "Fire cannons! " + w.getOccupant(location).takeHit(this.getStrength()) + " " + w.getOccupant(location).takeHit(this.getStrength());
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
}



