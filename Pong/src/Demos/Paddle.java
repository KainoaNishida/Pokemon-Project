package Demos;

import java.awt.*;

public class Paddle extends Rectangle {

    private Point initialLocation;

    public Paddle(int x, int y) {
        super(x, y, 15, 100);

        this.initialLocation = new Point(x, y);
    }

    public void resetLocation() {
        this.setLocation(this.initialLocation);
    }

}
