
package Battleship;

public class Cruiser extends ScoutBoat{
	public Cruiser(int team, Coordinates c, int dir) {
		super(team, c, dir, 3, 3);
	}
	
	public String getID() {
		return "C" + this.getTeam();
	}
	
	public String getActions() {
		return "Choose any of the following actions for the Cruiser:\n1. Move\n2. Turn left\n3. Turn right";

	}
	
	public String act(int[] choices, World w) {
		String actions = "";
		for(int choice: choices) {
			if(choice == 1) {
				actions += this.move(w) + "\n";
			}
			if(choice == 2) {
				actions += this.turn(-1) + "\n";
			}
			if (choice == 3) {
				actions += this.turn(1) + "\n";
			}
		}
		return actions;	
	}
}

