package Battleship;

public class World {

	public static final int NORTH = 0, NORTHEAST = 1, EAST = 2, 
	SOUTHEAST = 3, SOUTH = 4, SOUTHWEST = 5, WEST = 6, NORTHWEST = 7;
	int width;
	int height;
	
	private Boat[][] map;
	
	
	public World(int width, int height) {
		this.width = width;
		this.height = height; 
		if(width < 4) { this.width = 4;}
		if(width > 10) { this.width = 10;}
		if(height < 4) { this.height = 4;}
		if(height > 10) { this.height = 10;}
		
		map = new Boat[this.height][this.width];
		
		for(Boat[] row: map) {
			for(Boat boat: row) {
				boat = null;
			}
		}
	}
	
	public int getWidth() {
		return map[0].length;
	}
	
	public int getHeight() {
		return map.length;
	}
	
	public Boat getOccupant(Coordinates coordinates) {

		return map[coordinates.getY()][coordinates.getX()];
	}
	
	public boolean isLocationValid(Coordinates coordinates) {
		if(coordinates.getY() < this.getHeight() && coordinates.getY() > 0 && coordinates.getX() < this.getWidth() && coordinates.getX() > 0) {
			return true;
		}
		return false;
	}
	
	public boolean isLocationOccupied(Coordinates coordinates) {

		if (this.getOccupant(coordinates) != null) {
			return true;
		}
		return false;
	}
	
	public boolean setOccupant(Boat boat, Coordinates coordinates) {
		if (!this.isLocationOccupied(coordinates) || boat == null) {
			map[coordinates.getY()][coordinates.getX()] = boat;
			if(boat != null) {
				boat.setLocation(coordinates);
			}
			return true;
		}
		return false;
	}
	
	public Coordinates getAdjacentLocation(Coordinates coordinates, int direction) {
		if(direction == 0) {
			return new Coordinates(coordinates.getX(), coordinates.getY()-1);
		}
		if(direction == 1) {
			return new Coordinates(coordinates.getX()+1, coordinates.getY()-1);
		}
		if(direction == 2) {
			return new Coordinates(coordinates.getX()+1, coordinates.getY());
		}
		if(direction == 3) {
			return new Coordinates(coordinates.getX()+1, coordinates.getY()+1);
		}
		if(direction == 4) {
			return new Coordinates(coordinates.getX(), coordinates.getY()+1);
		}
		if(direction == 5) {
			return new Coordinates(coordinates.getX()-1, coordinates.getY()+1);
		}
		if(direction == 6) {
			return new Coordinates(coordinates.getX()-1, coordinates.getY());
		}
		if(direction == 7) {
			return new Coordinates(coordinates.getX()-1, coordinates.getY()-1);
		}
		return null;
	}
	
	public String drawTeamMap(Boat[] barray, int view) {
		String[] letters = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"};
		String map1 = "@ ";
		String map2 = "@ ";
		String[][] teamMap = new String[this.getHeight()][this.getWidth()];
		int team = barray[0].getTeam();
		
		for(int j=0; j<map.length; j++) {
			for(int k=0; k<map[j].length; k++) {
				teamMap[j][k] = "###";
			}
		}
	
		for(int i=1; i <= this.getWidth(); i++) {
			map1 += " "+i+" ";
			map2 += " "+i+" ";
		}
		map1 += "\n";
		map2 += "\n";
		

		if(view==1 || view == 2 || view == 3) {
			for(int j=0; j<map.length; j++) {
				map1 += letters[j]+ " ";
				for(int k=0; k<map[j].length; k++) {
					map1 += teamMap[j][k];
				}
				map1 += "\n";
			}
		}
		
		
		if(view==1) {
			return map1;
		}
		

		if(view==2 || view == 3) {
			for(Boat b: barray) {
				if(b.getTeam() == team) {	
					if (view == 2) {
						teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getDirection()+b.getID();
					}
					if (view == 3) {
						teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getHealth()+b.getID();
					}
					int left = b.getLocation().getY() - b.getVision();
					int right = b.getLocation().getY() + b.getVision();
					int top = b.getLocation().getX() - b.getVision();
					int bottom = b.getLocation().getX() + b.getVision();
					
					if (left < 0) {
						left = 0;
					}
					if (right > this.getWidth()-1) {
						right = this.getWidth()-1;
					}
					if (top < 0) {
						top = 0;
					}
					if (bottom > this.getHeight()-1) {
						bottom = this.getHeight()-1;
					}	
					for(int j=left; j <= right; j++) {
						for(int k=top; k<= bottom; k++) {
							if(teamMap[j][k] == "###") {
								teamMap[j][k] = "~~~";
							}
						}
					}
				}
			}
			for(Boat[] array: this.map)	{
				for(Boat b: array) {
					if(b!= null) {	
						if(b.getTeam() != team) {
							
							if(teamMap[b.getLocation().getY()][b.getLocation().getX()] == "~~~") {
								if(view == 2) {
									teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getDirection()+b.getID();
								}
								if (view == 3) {
									teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getHealth()+b.getID();
								}
								
							}
						}
					}
				}
			}
			
			
			for(Boat b: barray) {
				if(b.getTeam() != team) {
					
					if(teamMap[b.getLocation().getY()][b.getLocation().getX()] == "~~~") {
						if(view == 2) {
							teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getDirection()+b.getID();
						}
						if (view == 3) {
							teamMap[b.getLocation().getY()][b.getLocation().getX()] = b.getHealth()+b.getID();
						}
						
					}
				}
			}
			
			for(int j=0; j<map.length; j++) {
				map2 += letters[j]+ " ";
				for(int k=0; k<map[j].length; k++) {
					map2 += teamMap[j][k];
				}
				map2 += "\n";
			}
			return map2;
		}
		return null;
	}
}




