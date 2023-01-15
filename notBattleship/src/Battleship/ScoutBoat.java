
package Battleship;

public abstract class ScoutBoat extends Boat{
	public ScoutBoat(int team, Coordinates location, int direction, int health, int vision) {
        super(team, location, direction, health, 1, vision);
    }
	
	public String takeHit(int attacks) {
		for(int num = 0; num < attacks; num++) {
			int random = (int)(Math.random()*4+1);
			if (random == 1) {
				super.takeHit(1);
				return this.toString() + " takes 1 damage.";
			}
		}
		return this.toString() + " has avoided the attack!";
	}
}

