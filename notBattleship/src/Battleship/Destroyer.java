
package Battleship;

public class Destroyer extends Boat implements Attacker{
	
	public Destroyer(int team, Coordinates c, int dir) {
		super(team, c, dir, 2, 2, 1);
	}
	
	public String getID() {
		return "D" + this.getTeam();
	}
	
	public String getActions() {
		return "Choose any of the following actions for the Destroyer:\n1. Move\n2. Turn left\n3. Turn right\n4. Attack";
	}
	
	public String act(int[] choices, World w) {
		String attacks = "";
		for(int choice: choices) {
			if(choice == 1) {
				attacks += this.move(w) + "\n";
			}
			if(choice == 2) {
				attacks += this.turn(-1) + "\n";
			}
			if (choice == 3) {
				attacks += this.turn(1) + "\n";
			}
			if (choice == 4) {
				attacks += this.attack(w) + "\n";
			}
		}
		return attacks;
	}
	
	public String attack(World w) {
		int team = this.getTeam();
		Coordinates location = w.getAdjacentLocation(this.getLocation(), this.getDirectionNum());
		
		for(int i=0; i < this.getVision(); i++) {
			if(w.isLocationValid(location))	{
				if(w.isLocationOccupied(location)) {
					if(w.getOccupant(location).getTeam() != team){
						return "" + w.getOccupant(location).takeHit(this.getStrength());
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
	
	public String takeHit(int attackStrength) {
		int attack = (int)(Math.random()*2+1);
		
		if(attack == 3) {
			return "" + this.takeHit(attackStrength);
		}
		else {
			return this.getID() + " avoids the attack!";

		}
			
	}
	
}
