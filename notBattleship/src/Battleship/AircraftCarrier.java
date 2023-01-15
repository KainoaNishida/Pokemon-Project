
package Battleship;

public class AircraftCarrier extends Boat implements Attacker{
	private boolean hasPlanes = true;
	
	public AircraftCarrier(int team, Coordinates c, int dir) {
		super(team, c, dir, 5, 1, 1);
	}
	
	public String getID() {
		return "A" + this.getTeam();
	}
	
	public String getActions() {
		String s = "Choose any of the following actions for the Aircraft Carrier:\n1. Move\n2. Turn left\n3. Turn right\n";
		if (this.hasPlanes == true) {
			s += "4. Launch planes";
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
				return this.attack(w);
			}
		}
		return null;
	}
	
	public String attack(World w) {
		int team = this.getTeam();
		String attacks = "Air Raid! ";
		boolean attack = false;
		double successRate = 1;
		double num = Math.random();
		
		if(this.hasPlanes == true) {
			for(int i=0; i < 8; i++) {
				Coordinates location = w.getAdjacentLocation(this.getLocation(), i);
				for(int j=0; j < this.getVision(); j++) {
					if(w.isLocationValid(location)) {
						if(w.isLocationOccupied(location)) {
							if(w.getOccupant(location).getTeam() != team){
								attack = true;
								attacks += w.getOccupant(location).takeHit(this.getStrength()) + " ";
								successRate = successRate * .8;
							}
						}
						location = w.getAdjacentLocation(location, this.getDirectionNum());
					}
					else {
						break;
					}
				}
			}
			if(attack == true) {
				if(num > successRate) {
					hasPlanes = false;
				}
				return attacks;
			}
			else{
				if(num > successRate) {
					hasPlanes = false;
				}
				return "There are no boats in range currently.";
			}
		}
		return this.getID() + " has no planes remaining.";
		
		
	}	
}
