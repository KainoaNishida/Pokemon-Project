import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;

import javax.swing.JFrame;

/* Ga - M needs to be written on the chest */
public class Game extends GameDriverV2 implements KeyListener, MouseListener, MouseMotionListener{
	SoundDriver s1;
	int textpage;
	int gamestate;
	int delay;
	int timer1;
	int timer2;
	int rand;
	int i;
	int f;
	int equippedholder;
	Rectangle start;
	int[] chestlock = new int[3];
	boolean rockcomplete;
	boolean chestcomplete;
	boolean treeopen;
	boolean statuecomplete;
	boolean flutecomplete;
	boolean altarcomplete;
	boolean notecomplete;
	boolean[] typepossibletext = new boolean[3];
	boolean rock1;
	boolean rock2;
	boolean rock3;
	boolean rock4;
	boolean rock5;
	boolean chest1;
	boolean chest2;
	boolean chest3;
	boolean ped1;
	boolean ped2;
	boolean ped3;
	boolean gamestart;
	boolean typing;
	boolean[] rockcombo = new boolean[5];
	int[] rockcombohelper = new int[5];
	Rectangle[] rockbuttons = new Rectangle[10];
	Rectangle[] chestbuttons = new Rectangle[6];
	Rectangle inv,tempBG, rightbutton, leftbutton, celebihitbox, backbutton, altarhitbox, treehitbox, rockhitbox, chesthitbox, dialgahitbox, h2phitbox, dialgatexthitbox, statueflutehitbox, altartypedhitbox, celebibackbutton, poemtypehitbox;
	BufferedImage title;
	BufferedImage cbg;
	BufferedImage chestcloseup, openchestcloseup, altar, statue, celebi, tree, opentree, rockactivated, paperpickup, papersprite, poem1, poem2, winner, cutscene3;
	BufferedImage inventory;
	BufferedImage rockcloseup;
	BufferedImage textbox;
	BufferedImage[] background = new BufferedImage[4];
	BufferedImage[] cutscenes = new BufferedImage[6];
	BufferedImage fluteinuse;
	
	Font loserfont = new Font("Impact", Font.BOLD, 100);
	Font winnerfont = new Font("Agency FB", Font.PLAIN, 80);
	Font notewords = new Font("Agency FB", Font.PLAIN, 40);
	Font timerfont = new Font("Impact", Font.PLAIN, 60);
	Font startfont = new Font("Impact", Font.PLAIN, 130);
	Font h2pfont = new Font("Impact", Font.PLAIN, 50);
	Font backfont = new Font("Impact", Font.PLAIN, 20);
	Font chestlockfont = new Font("Impact", Font.PLAIN, 10);
	Font itemfont  = new Font("Impact", Font.PLAIN, 15);
	Font igfont = new Font("Arial Narrow", Font.PLAIN, 50);
	Font text = new Font("Agency FB", Font.PLAIN, 25  );
	Font typepossible = new Font("Agency FB", Font.PLAIN, 20);
	
	String description;
	String altartyped;
	String altartarget;
	String notetyped;
	String notetarget;
	String notetarget2;
	String statuetyped;
	String statuetarget; 
	
	boolean items[] = new boolean[6];
	BufferedImage[] itemiconimages = new BufferedImage[3];
	BufferedImage[] itemimages = new BufferedImage[6];
	Rectangle paper1, paper2, paper3, paper4, key, flute, keyhitbox, treekeyhitbox, treenotehitbox, wholescreen;
	boolean equipped[] = new boolean[6];
	boolean showkey;
	
	Rectangle red, orange, yellow, green, blue, indigo, violet;
	int pressed;
	boolean[] flutecode = new boolean[5];
	
	
	public Game() {
		i=0;
		f=0;
		this.addKeyListener(this);
		this.addMouseListener(this);
		this.addMouseMotionListener(this);
		inv = new Rectangle(15,585, 310,75);
		paperpickup = this.addImage("paperitem.png");
		winner = this.addImage("you won.jpg");
		cutscene3 = this.addImage("cutscene 3.jpg");
		
		itemimages[4] = this.addImage("rsz_bigkey.png");
		itemimages[5] = this.addImage("flute.png");
		rockactivated = this.addImage("rock Activate.jpg");
		
		cutscenes[0] = this.addImage("cutscene 1.jpg");
		cutscenes[1] = this.addImage("cutscene2.jpg");
		cutscenes[2] = this.addImage("cutscene 1.jpg");
		cutscenes[3] = this.addImage("cutscene 1.jpg");
		cutscenes[4] = this.addImage("cutscene 1.jpg");
		cutscenes[5] = this.addImage("cutscene 1.jpg");
		papersprite = this.addImage("paper sprite 1.png");
		
		itemiconimages[1] = this.addImage("keyicon.png");
		itemiconimages[2] = this.addImage("fluteicon.png");
		fluteinuse = this.addImage("fluteitem.png");
		
		altartyped = "";
		altartarget = "flora";
		notetyped = "";
		notetarget = "past present future";
		notetarget2 = "past present and future";
		statuetyped = "";
		statuetarget = "elm";
		
		for(int i = 0; i < 6; i++){
			items[i] = false;
		}
		//0 = initial
		//1 = altar
		//2 = tree
		//3 = rock
		//4 = key
		//5 = flute
		items[0] = true;
		items[1] = true;
		
		poem1 = this.addImage("poem1.png");
		poem2 = this.addImage("poem2.png");
		
		notecomplete = false; 
		
		poemtypehitbox = new Rectangle(730, 570, 530, 100);
		altartypedhitbox = new Rectangle(370, 530, 310, 130);
		dialgatexthitbox = new Rectangle(460, 350, 580,140);
		paper1 = new Rectangle(20,589,42,66);		
		paper2 = new Rectangle(67,589, 47,66);
		paper3 = new Rectangle(119,589,46,66);
		paper4 = new Rectangle(171,589,44,66);
		key = new Rectangle(223,589,43,66);
		flute = new Rectangle(274,589,43,66);
		keyhitbox = new Rectangle(600, 50, 342, 180);
		statueflutehitbox = new Rectangle(400,50,683,360);
		showkey = false; 
		notecomplete = false;
		treekeyhitbox = new Rectangle(450, 100, 500, 350);
		treenotehitbox = new Rectangle(400, 220, 500, 350);
		for(int i = 0; i <3; i++){
			typepossibletext[i] = false;
		}
		
		textpage = -1;
		
		chestcloseup = this.addImage("chestcloseup.jpg");
		openchestcloseup = this.addImage("openchestcloseup.jpg");
		altar = this.addImage("altar.jpg");
		statue = this.addImage("statue.jpg");
		celebi = this.addImage("celebi.jpg");
		tree = this.addImage("treehole.jpg");
		opentree = this.addImage("cubby.jpg");
		textbox = this.addImage("textbox.png");
		
		chestlock[0] = 0;
		chestlock[1] = 0;
		chestlock[2] = 0;
		
		rockcombo[0] = false;
		rockcombo[1] = false;
		rockcombo[2] = false;
		rockcombo[3] = false;
		rockcombo[4] = false;
		
		rockbuttons[0] = new Rectangle(623,338,75,45);
		rockbuttons[1] = new Rectangle(712,320,79,55);
		rockbuttons[2] = new Rectangle(800,310,80,48);
		rockbuttons[3] = new Rectangle(890,300,80,45);
		rockbuttons[4] = new Rectangle(980,290,70,52);
		rockbuttons[5] = new Rectangle(625,420,75,45);
		rockbuttons[6] = new Rectangle(720,413,85,45);
		rockbuttons[7] = new Rectangle(820,400,75,48);
		rockbuttons[8] = new Rectangle(903,387,80,47);
		rockbuttons[9] = new Rectangle(990,380,77,44);
		
		
		chestbuttons[0] = new Rectangle(501,628,90,45);
		chestbuttons[1] = new Rectangle(643,635,90,45);
		chestbuttons[2] = new Rectangle(803,630,90,45);
		
		chestbuttons[3] = new Rectangle(503,513,90,45);
		chestbuttons[4] = new Rectangle(641,520,90,45);
		chestbuttons[5] = new Rectangle(788,515,90,45);
		
		String[] sound = new String[12];
		sound[0] = "BornToBeAWinner.wav";
		sound[1] = "Eternaforest.wav";
		sound[2] = "suspense.wav";
		sound[3] = "microwave.wav";
		sound[4] = "pickedupitem.wav";
		sound[5] = "1.wav";
		sound[6] = "2.wav";
		sound[7] = "3.wav";
		sound[8] = "4.wav";
		sound[9] = "5.wav";
		sound[10] = "6.wav";
		sound[11] = "7.wav";
		
		
		s1 = new SoundDriver(sound);
		description = "";
		dialgahitbox = new Rectangle(630,570,300,110);
		h2phitbox = new Rectangle(1020,25,300,70);
		backbutton = new Rectangle(1035,570,50,50);
		celebibackbutton = new Rectangle(1185,320,50,50);
		celebihitbox = new Rectangle(455,570,125,70);
		treehitbox = new Rectangle(1060,25,100,100);
		rockhitbox = new Rectangle(1050,450,250,150);
		chesthitbox = new Rectangle(995,590,70,70);
		tempBG = new Rectangle(0,0,1366,720);
		leftbutton = new Rectangle(10,320,50,50);
		rightbutton = new Rectangle(1290,320,50,50);
		altarhitbox = new Rectangle(1190,410,120,70);
		start = new Rectangle(400,460,500,150);
		gamestate = 0;
		rand = 0;
		rockcomplete = false;
		chestcomplete = false;
		treeopen = false;
		statuecomplete = false;
		altarcomplete = false;
		flutecomplete = false;
		gamestart = false;
		rock1 = false;
		rock2 = false;
		rock3 = false;
		rock4 = false;
		rock5 = false;
		chest1 = false;
		chest2 = false;
		chest3 = false;
		ped1 = false;
		ped2 = false;
		ped3 = false;
		typing = false;
		inventory = this.addImage("lameassinventory.png");
		rockcloseup = this.addImage("rock.jpg");
		title = this.addImage("titlelogo.png");
		cbg = this.addImage("cbg.png");
		background[0] = this.addImage("bgfront.jpg");
		background[1] = this.addImage("bgright.jpg");
		background[2] = this.addImage("bgback.jpg");
		background[3] = this.addImage("bgleft.jpg");
		timer1 = 20;
		timer2 = 0;
		delay = 30;
		wholescreen = new Rectangle(0,0,1366,720);
		
		for(int i =0; i<6; i++){
			equipped[i] = false;
		}
		equippedholder = 0;
		
		
		red = new Rectangle(280, 490, 100, 70);
		orange = new Rectangle(400, 490, 100, 70);
		yellow = new Rectangle(523, 490, 100, 70);
		green = new Rectangle(640, 490, 100, 70);
		blue = new Rectangle(755, 485, 100, 70);
		indigo = new Rectangle(877, 485, 100, 70); 
		violet = new Rectangle(995, 490, 100, 70);
		pressed = 0;
		for(int i = 0; i<5; i++){
			flutecode[i] = false;
		}
		
	}	


	public static void main(String[] args){
		JFrame j1 = new JFrame();
		j1.setSize(1366, 720);
		j1.setTitle("Pok�mon Awakening");
		j1.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		j1.add(new Game());
		j1.setVisible(true);
	}
	
	

	@Override
	public void draw(Graphics2D win) {
		if(timer1 == 0 && timer2 == 0){
			if(gamestate > 5 && gamestate < 19){
				gamestate = 22;
			}
		}
		if(gamestate == 0){
			win.drawImage(cbg, null, 0, 0);
			win.drawImage(title, null, 160, 250);
			win.fill(start);
			win.fill(h2phitbox);
			fonting(startfont, Color.WHITE, win);
			win.drawString("START", 485, 585);
			fonting(h2pfont, Color.WHITE, win);
			win.drawString("How to Play", 1055, 80);
			
		}
		
		if(gamestate == 2){ // how to play
			description = "how to play";
			drawgamestate(win);
			win.setColor(Color.BLACK);
			win.fill(wholescreen);
			win.setColor(Color.WHITE);
			win.fill(backbutton);
			drawbackbutton(win);
			
			
			win.setColor(Color.WHITE);
			win.setFont(text);
			win.drawString("Pokemon Awakening is a puzzle based game that involves you having to crack a multitude of complex",25,50);
			win.drawString("locks and passcodes to acquire the necessary items to progress through and beat the game. You'll",25,90);
			win.drawString("start off with an inventory in the bottom left hand corner, which will increase in size as you ",25,130);
			win.drawString("obtain more items. To equip an item, simply click on it and to unequip it, press escape. Also, if",25,170);
			win.drawString("you open up a text box, if possible you can scroll to the next page by left clicking. There are also",25,210);
			win.drawString("places where you will need to type in passwords. If it's possible to type in an area, text will appear",25,250);
			win.drawString("as an indication. Simply click, type in the password, and hit enter to both clear and check to see if",25,290);
			win.drawString("what you typed is correct. There will be a massive visual change when the correct password is entered.",25,330);
			win.drawString("You will have 20 minutes to complete the game indicated by a timer in the upper left. Good luck.",25,370);
			win.drawString("(Click the white box to go back to the start screen)", 25, 450);
			
		}
		/*
		 * win.drawString("", 50, 520);
		 */
		
		if(gamestate == 3){ // cutscene 1
			description = "cutscene 1";
			drawgamestate(win);
			win.drawImage(cutscenes[0], null, 0, 0);
			win.setFont(text);
			win.setColor(Color.WHITE);
			win.drawImage(textbox, null, 0, 450);
			win.setColor(Color.BLACK);
			win.drawString("Leader of Team Rocket, Giovanni, has found a way to tame even the legendary pokemon. By",50,520);
			win.drawString("turning them into shadow pokemon, Team Rocket is able to create pokemon devoid of all",50,560);
			win.drawString("emotions. As a result,these souless fighting machines blindly follow their masters. With" ,50,600);
			win.drawString("this power, Team Rocket has taken over the city and plots to take control of the Johto region. ",50,640);
			
			
			
		}
		if(gamestate == 4){ // cutscene 2
			description = "cutscene 2";
			drawgamestate(win);
			win.drawImage(cutscenes[1], null, -10,-5);
			win.setFont(text);
			win.setColor(Color.WHITE);
			win.drawImage(textbox, null, 0, 450);
			win.setColor(Color.BLACK);
			win.drawString("The only legendary that was able to withstand Team Rocket's spell was Celebi. Purer than",50,520);
			win.drawString("any other pokemon, Team Rocket was unable to corrupt its heart and take control. However,",50,560);
			win.drawString("they did manage to put it into a deep slumber and encapsule it in its home, Ilex Forest," ,50,600);
			win.drawString("thus preventing it from using any of its powers to help the others.",50,640);
		}
		if(gamestate == 5){ // cutscene 3
			description = "cutscene 3";
			drawgamestate(win);
			
			win.drawImage(cutscene3 ,null, 0, 0);
			win.setFont(text);
			win.setColor(Color.WHITE);
			win.drawImage(textbox, null, 0, 450);
			win.setColor(Color.BLACK);
			win.drawString("You're the only one we can send to help free celebi. Deep within the forest you'll find",50,520);
			win.drawString("Celebi's altar along with a plethora of puzzles you need to solve in order to wake up Celebi.",50,560);
			win.drawString("I'm giving you a note and a poem that is said to have a part in solving the puzzles. I'll" ,50,600);
			win.drawString("place them in the inventory at the bottom left part of your screen. Good luck!",50,640);
		}
		if(gamestate == 6){ // front far view
			if(gamestart == false){
				gamestart = true;
			}
			description = "front far view";
			drawgamestate(win);
			win.drawImage(background[0], null, 0, 0);
			win.fill(leftbutton);
			win.fill(rightbutton);
			drawsidebuttons(win);
			win.fill(inv);
		}
		if(gamestate == 7){ // right far view
			description = "right far view";
			drawgamestate(win);
			win.drawImage(background[1], null, 0, 0);
			win.fill(leftbutton);
			win.fill(rightbutton);
			drawsidebuttons(win);
		}
		if(gamestate == 8){ // back far view
			description = "back far view";
			drawgamestate(win);
			win.drawImage(background[2], null, 0, 0);
			win.fill(leftbutton);
			win.fill(rightbutton);
			drawsidebuttons(win);
		}
		if(gamestate == 9){ // left far view
			description = "left far view";
			drawgamestate(win);
			win.drawImage(background[3], null, 0, 0);
			win.fill(leftbutton);
			win.fill(rightbutton);
			drawsidebuttons(win);
		}
		if(gamestate == 10){ // initial altar close-up
			description = "initial altar close-up";
			drawgamestate(win);
			win.drawImage(altar,null,0,0);
			win.fill(backbutton);
			drawbackbutton(win);
			fonting(timerfont, Color.WHITE, win);
			win.drawString(altartyped, 455,615);
			if(altarcomplete){
				win.setColor(Color.YELLOW);
				win.drawImage(paperpickup, null, 300, 500);
			}
			if(typepossibletext[0]){
				win.setColor(Color.WHITE);
				win.setFont(typepossible);
				win.drawString("(Click and type to enter a passcode)", 700, 500);
			}

		}
		if(gamestate == 11){ // unlocked altar close-up
			description = "unlocked altar close-up";
			drawgamestate(win);
		}
		if(gamestate == 12){ // celebi close-up
			if(flutecomplete){
				gamestate = 19;
			}
			description = "celebi close-up";
			drawgamestate(win);
			win.drawImage(celebi, null, 0, 0);
			win.fill(celebibackbutton);
			drawcelebibackbutton(win);
			
			
			if(equipped[5] == true){
				win.drawImage(fluteinuse, null, -4, 180);
			}
		}
		if(gamestate == 13){ // key tree close-up initial
			if(treeopen == true){
				gamestate++;
			}
			description = "key tree close-up initial";
			drawgamestate(win);
			win.drawImage(tree, null, 0, 0);
			win.fill(backbutton);
			drawbackbutton(win);
			
			
		}
		if(gamestate == 14){ // key tree close-up unlocked
			description = "key tree close-up unlocked";
			drawgamestate(win);
			win.drawImage(opentree, null, 0, 0);
			win.fill(backbutton);
			drawbackbutton(win);
			if(items[3] == false){
				win.setColor(Color.YELLOW); 
				win.drawImage(paperpickup, null, 390, 360);
			}
		}
		if(gamestate == 15){ // rock close-up
			if(rockcomplete){
				gamestate = 23;
			}
			description = "rock close-up";
			drawgamestate(win);
			win.drawImage(rockcloseup, null, 0, 0);
			if(rockcomplete){
				win.drawString("Rock Puzzle Complete (Scroll should appear)", 200, 350);
			}
			win.fill(backbutton);
			drawbackbutton(win);
		}
		if(gamestate == 16){ // chest close-up initial
			if(chestcomplete == true){
				gamestate++;
			}
			description = "chest close-up initial";
			drawgamestate(win);
			win.drawImage(chestcloseup, null, -15, -35);
			win.fill(backbutton);
			drawbackbutton(win);
			
			fonting(h2pfont, Color.WHITE, win);
			win.drawString(""+chestlock[0], 532, 613);
			win.drawString(""+chestlock[1], 673, 620);
			win.drawString(""+chestlock[2], 825, 620);
			
			
			
		}
		if(gamestate == 17){ //chest close-up unlocked
			description = "chest close-up unlocked";
			drawgamestate(win);
			win.drawImage(openchestcloseup, null, -15,-35);
			win.fill(backbutton);
			drawbackbutton(win);
			
			if(showkey){
				win.drawImage(itemimages[4],null, 600, 50);
			}
		}
		if(gamestate == 18){ //Pedestal Close-Up
			description = "Pedestal Close-Up";
			drawgamestate(win);
			win.drawImage(statue, null, 0, 0);
			win.fill(backbutton);
			drawbackbutton(win);
			win.setFont(timerfont);
			if(typing){
			win.drawString(statuetyped, 700, 445);
			}
			if(statuecomplete){
				win.drawImage(itemimages[5], null, 400,50);
			}
			if(typepossibletext[1]){
				win.setColor(Color.WHITE);
				win.setFont(typepossible);
				win.drawString("(Click and type to enter a passcode)", 850, 320);
			}
		}
		if(gamestate == 19){ // cut scene - 4
			description = "cut scene - 4";
			drawgamestate(win);
			win.drawImage(winner, null, 0, 0);
			win.setFont(winnerfont);
			win.setColor(Color.YELLOW);
			win.drawString("Congratulations!", 550, 600);
		}
		if(gamestate == 20){ // cut scene - 5
			description = "cut scene - 5";
			drawgamestate(win);
		}
		if(gamestate == 21){ // cut scene - 6
			description = "cut scene - 6";
			drawgamestate(win);
		}
		if(gamestate == 22){ // end game screen
			description = "end game screen";
			drawgamestate(win);
			win.setColor(Color.BLACK);
			win.fill(wholescreen);
			win.setColor(Color.RED);
			win.setFont(loserfont);
			win.drawString("GAME OVER", 400, 400);
			
		}
		if(gamestate == 23){ // rock close-up
			description = "rock close-up";
			drawgamestate(win);
			win.drawImage(rockactivated, null, 0, 0);
			win.fill(backbutton);
			drawbackbutton(win);
		
		}
		
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)){ // in game gamestates
			fonting(timerfont, Color.WHITE, win);
			if(timer2 >= 10){ //use only for certain gamestates
				
				win.drawString(timer1 + ":" + timer2, 20, 70);
			}
			else{
				win.drawString(timer1 + ":0" + timer2, 20, 70);
			}
			win.drawImage(inventory, null, 15,585);
			if(s1.isPlaying(1) == false){
				s1.play(1);
			}
			
			
			//below is all item rectangles drawn
			win.setColor(Color.YELLOW);
			if(items[0]){
				if(equipped[0]){
					win.draw(paper1);
					
				}
			}
			if(items[1]){
				if(equipped[1]){
					win.draw(paper2);
					
				}
			}
			if(items[2]){
				if(equipped[2]){
					win.draw(paper3);
					
				}
			}
			if(items[3]){
				if(equipped[3]){
					win.draw(paper4);
				}
			}
			if(items[4]){
				if(equipped[4]){
					
					win.draw(key);
				}
			}
			if(items[5]){
				if(equipped[5]){
					
					win.draw(flute);
				}
			}
			
			if(equipped[1] && !notecomplete){
				win.setColor(Color.YELLOW);
				win.drawImage(poem1, null, 0, 0);
				if(typing){
					win.setFont(notewords);
					win.setColor(Color.BLACK);
					win.drawString(notetyped, 750, 600);
					
				}
				if(typepossibletext[2]){
					win.setColor(Color.WHITE);
					win.setFont(typepossible);
					win.drawString("(Click and type to enter a passcode)", 740, 635);
				}
			}
			if(equipped[1] && notecomplete){
				win.drawImage(poem2, null, 0,0);
			}
		}
		
		else{
			s1.stop(1);
		}
		
		if(gamestate < 3){ //intro 
			if(s1.isPlaying(0) == false){
				s1.play(0);
				
			}
		}
		else{
			s1.stop(0);
		}
		
		if(gamestate >= 3 && gamestate <= 5){ //first cut scenes
			if(s1.isPlaying(2) == false){
				s1.play(2);
				
			}
		}
		else{
			s1.stop(2);
		}
		
		if(gamestate > 5 && gamestate <19){
			if(gamestart == true){ //timer stuff
				if(delay == 0){
					if(timer2 == 0){
						timer1--;
						timer2 = 59;
					}
					timer2 -= 1;
					delay = 30;
				}
				delay--;
				if(timer1 <= 0 && timer2 <=0){
					gamestart = false;
					//also change gamestate to end
				}
			}
		}
			
		//below is placeholder for pictures of items & also the text boxes
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)){
			win.setColor(Color.GREEN);
			win.setFont(itemfont);
			if(items[0]){
				win.drawImage(papersprite, null, 23, 589);
			}
			if(items[1]){
				win.drawImage(papersprite, null, 70, 589);
			}
			if(items[2]){
				
				win.drawImage(papersprite, null, 122, 589);
			}
			if(items[3]){

				win.drawImage(papersprite, null, 173, 589);
			}
			if(items[4]){

				win.drawImage(itemiconimages[1], null, 231, 600);
			}
			if(items[5]){
				win.drawImage(itemiconimages[2], null, 277, 592);
				//HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
			}
			
			if(equipped[0] || equipped[2] || equipped[3]){
				//IMAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
				win.setColor(Color.GREEN);
				win.setFont(igfont);
				fonting(text, Color.BLACK, win);
				win.drawImage(textbox, null, 0,454);
				
				/*  TEXT template
				 * 		win.drawString("", 50, 520);
						win.drawString("", 50, 560);
						win.drawString("", 50, 600);
						win.drawString("", 50, 640);
				 */
				
				if(equipped[0]){
					if(textpage == 0){
						win.drawString("Celebi is one of the rare legendary pokemon and in the pokedex is #251. It's one of the two", 50, 520);
						win.drawString("time travel pokemon, Dialga being the other. Hence, it has the ability to go back to the past", 50, 560);
						win.drawString("and stop team rocket before they can ever initiate their evil plan. However, as stated before,", 50, 600);
						win.drawString("it's in a deep slumber, and the only way it can be awoken is by playing the flute of Dialga.", 50, 640);
					}
					if(textpage == 1){
						win.drawString("You need to find the flute, and play the correct tune to wake up celebi before team rocket", 50, 520);
						win.drawString("can completely take over the world. We're counting on you. Good Luck.", 50, 560);
						win.drawString("And remember. AL : L", 50, 600);
						win.drawString("-Professor Oak", 50, 640);
					}
					
				}
				
				if(equipped[2]){
					
						win.drawString("Di - e", 50, 520);
					
				}
				
				if(equipped[3]){
					
						win.drawString("Ga - M", 50, 520);
					
				}
				
				
			}
		}
		
		
	}

	public void fonting(Font f1, Color c1, Graphics2D win){
		win.setColor(c1);
		win.setFont(f1);
	}
	
	public void drawgamestate(Graphics2D win){
		win.setColor(Color.CYAN);
		win.fill(tempBG);
		fonting(timerfont, Color.BLACK, win);
		win.drawString(description,520,130);
		win.drawString(""+gamestate,630,200);
	}
	
	public void drawsidebuttons(Graphics2D win){
		fonting(h2pfont, Color.WHITE, win);
		win.drawString("<-", 13,365);
		win.drawString("->", 1293,365);
	}
	
	public void drawbackbutton(Graphics2D win){
		fonting(backfont, Color.WHITE, win);
		win.drawString("BACK", 1038, 602);
	}
	
	public void drawcelebibackbutton(Graphics2D win){
		fonting(backfont, Color.WHITE, win);
		win.drawString("BACK", 1188,352);
	}
	
	@Override
	public void keyPressed(KeyEvent arg0) {
		if(arg0.getKeyCode() == KeyEvent.VK_ESCAPE){
			for(int i =0; i<6; i++){
				equipped[i] = false;
				equippedholder = 0;
				typing = false;
				altartyped = "";
				notetyped = "";
				statuetyped = "";
				
			}
			textpage = -1;
		}
		//typing all typing fuck my life
		if(typing){
			if(arg0.getKeyCode() == KeyEvent.VK_Q){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "q";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "q";
					}
				}
				
				if(equipped[1]){
					notetyped += "q";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_W){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "w";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "w";
					}
				}
				
				if(equipped[1]){
					notetyped += "w";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_E){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "e";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "e";
					}
				}
				
				if(equipped[1]){
					notetyped += "e";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_R){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "r";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "r";
					}
				}
				
				if(equipped[1]){
					notetyped += "r";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_T){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "t";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "t";
					}
				}
				
				if(equipped[1]){
					notetyped += "t";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_Y){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "y";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "y";
					}
				}
				
				if(equipped[1]){
					notetyped += "y";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_U){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "u";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "u";
					}
				}
				
				if(equipped[1]){
					notetyped += "u";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_I){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "i";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "i";
					}
				}
				
				if(equipped[1]){
					notetyped += "i";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_O){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "o";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "o";
					}
				}
				
				if(equipped[1]){
					notetyped += "o";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_P){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "p";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "p";
					}
				}
				
				if(equipped[1]){
					notetyped += "p";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_A){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "a";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "a";
					}
				}
				
				if(equipped[1]){
					notetyped += "a";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_S){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "s";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "s";
					}
				}
				
				if(equipped[1]){
					notetyped += "s";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_D){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "d";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "d";
					}
				}
				
				if(equipped[1]){
					notetyped += "d";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_F){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "f";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "f";
					}
				}
				
				if(equipped[1]){
					notetyped += "f";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_Q){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "q";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "q";
					}
				}
				
				if(equipped[1]){
					notetyped += "q";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_G){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "g";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "g";
					}
				}
				
				if(equipped[1]){
					notetyped += "g";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_H){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "h";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "h";
					}
				}
				
				if(equipped[1]){
					notetyped += "h";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_J){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "j";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "j";
					}
				}
				
				if(equipped[1]){
					notetyped += "j";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_K){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "k";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "k";
					}
				}
				
				if(equipped[1]){
					notetyped += "k";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_L){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "l";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "l";
					}
				}
				
				if(equipped[1]){
					notetyped += "l";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_Z){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "z";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "z";
					}
				}
				
				if(equipped[1]){
					notetyped += "z";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_X){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "x";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "x";
					}
				}
				
				if(equipped[1]){
					notetyped += "x";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_C){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "c";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "c";
					}
				}
				
				if(equipped[1]){
					notetyped += "c";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_V){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "v";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "v";
					}
				}
				
				if(equipped[1]){
					notetyped += "v";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_M){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "m";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "m";
					}
				}
				
				if(equipped[1]){
					notetyped += "m";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_SPACE){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += " ";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += " ";
					}
				}
				
				if(equipped[1]){
					notetyped += " ";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_B){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "b";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "b";
					}
				}
				
				if(equipped[1]){
					notetyped += "b";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_N){
				if(gamestate == 10){
					if(!equipped[1]){
						altartyped += "n";
					}
				}
				
				if(gamestate == 18){
					if(!equipped[1]){
						statuetyped += "n";
					}
				}
				
				if(equipped[1]){
					notetyped += "n";
				}
			}
			if(arg0.getKeyCode() == KeyEvent.VK_DELETE){
				altartyped.substring(0, altartyped.length()-2);
				notetyped.substring(0, altartyped.length()-2);
				statuetyped.substring(0, altartyped.length()-2);
			}
			if(arg0.getKeyCode() == KeyEvent.VK_ENTER){
				typing = false;
				if(altartyped.equals(altartarget)){
					if(f==0){
						altarcomplete = true;
					}
					f++;
				}
				if(notetyped.equals(notetarget) || notetyped.equals(notetarget2)){
					notecomplete = true;
				}
				
				
				
				if(statuetyped.equals(statuetarget)){
					if(i == 0){
						statuecomplete = true; 
					}
					i++;
				}
				
				altartyped = "";
				notetyped = "";
				statuetyped = "";
				
			
			
				
			}
			
		}
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		
		
	}


	@Override
	public void keyTyped(KeyEvent arg0) {
		
		
	}


	@Override
	public void mouseClicked(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		if(gamestate == 0 && start.contains(arg0.getPoint())){
			gamestate = 3;
		}
		else if(gamestate == 0 && h2phitbox.contains(arg0.getPoint())){
			gamestate = 2;
		}
		else if(gamestate == 3 || gamestate  == 4 || gamestate == 5){
			gamestate ++;
		}
		else if((gamestate == 6 || gamestate == 7 || gamestate == 8) && rightbutton.contains(arg0.getPoint())){
			gamestate ++;
		}
		else if((gamestate == 7 || gamestate == 8 || gamestate == 9) && leftbutton.contains(arg0.getPoint())){
			gamestate --;
		}
		else if(gamestate == 9 && rightbutton.contains(arg0.getPoint())){
			gamestate = 6;
		}
		else if(gamestate == 6 && leftbutton.contains(arg0.getPoint())){
			gamestate = 9;
		}
		else if(gamestate == 6 && celebihitbox.contains(arg0.getPoint())){
			gamestate = 12;
		}
		else if(gamestate == 12 && celebibackbutton.contains(arg0.getPoint())){
			gamestate = 6;
			pressed = 0;
			for(int i = 0; i < 5; i++){
				flutecode[i] = false;
			}
			
		}
		else if(gamestate == 6 && altarhitbox.contains(arg0.getPoint())){
			gamestate = 10;
		}
		else if((gamestate == 10 || gamestate == 11)&& backbutton.contains(arg0.getPoint())){
			gamestate = 6;
			typing = false;
			altartyped = "";
			notetyped = "";
			statuetyped = "";
			typing = false;
			altartyped = "";
			notetyped = "";
			statuetyped = "";
		}
		else if(gamestate == 7 && treehitbox.contains(arg0.getPoint())){
			gamestate = 13;
		}
		else if((gamestate == 13 || gamestate == 14) && backbutton.contains(arg0.getPoint())){
			gamestate = 7;
		}
		else if(gamestate == 13){
			if(items[4] == true){
				if(equipped[4] == true){
					if(treekeyhitbox.contains(arg0.getPoint())){
						treeopen = true;
					}
				}
			}
		}
		else if(gamestate == 7 && rockhitbox.contains(arg0.getPoint())){
			gamestate = 15;
		}
		else if((gamestate == 15 || gamestate == 23)&& backbutton.contains(arg0.getPoint())){
			gamestate = 7;
			for(int i = 0; i < 5; i++){
				rockcombo[i] = false;
				rockcombohelper[i] = 0;
			}
		}
		else if(gamestate == 9 && chesthitbox.contains(arg0.getPoint())){
			gamestate = 16;
		}
		else if((gamestate == 16 || gamestate == 17) && backbutton.contains(arg0.getPoint())){
			gamestate = 9;
		}
		else if(gamestate == 8 && dialgahitbox.contains(arg0.getPoint())){
			gamestate = 18;
		}
		else if(gamestate == 18 && backbutton.contains(arg0.getPoint())){
			gamestate = 8;
			typing = false;
			altartyped = "";
			notetyped = "";
			statuetyped = "";
		}
		else if(gamestate == 2 && backbutton.contains(arg0.getPoint())){
			gamestate = 0;
		}
		else if(gamestate == 16){
			if(chestbuttons[0].contains(arg0.getPoint())){
				if(chestlock[0] > 0){
					chestlock[0]--;
				}
				else{
					chestlock[0] = 9;
				}
			}
			if(chestbuttons[1].contains(arg0.getPoint())){
				if(chestlock[1] > 0){
					chestlock[1]--;
				}
				else{
					chestlock[1] = 9;
				}
			}
			if(chestbuttons[2].contains(arg0.getPoint())){
				if(chestlock[2] > 0){
					chestlock[2]--;
				}
				else{
					chestlock[2] = 9;
				}
			}
			if(chestbuttons[3].contains(arg0.getPoint())){
				if(chestlock[0] < 9){
					chestlock[0]++;
				}
				else{
					chestlock[0] = 0;
				}
			}
			if(chestbuttons[4].contains(arg0.getPoint())){
				if(chestlock[1] < 9){
					chestlock[1]++;
				}
				else{
					chestlock[1] = 0;
				}
			}
			if(chestbuttons[5].contains(arg0.getPoint())){
				if(chestlock[2] < 9){
					chestlock[2]++;
				}
				else{
					chestlock[2] = 0;
				}
			}
			if(chestlock[0] == 2 && chestlock[1] == 5 && chestlock[2] == 1 && rand == 0){
				chestcomplete = true;
				showkey = true;
				rand++;
			}
			
		}
		if(gamestate == 17){
			if(showkey == true){
				if(keyhitbox.contains(arg0.getPoint())){
					items[4] = true;
					showkey = false;
					s1.play(4);
				}
			}
		}
		if(gamestate == 18 && dialgatexthitbox.contains(arg0.getPoint())){
			if(i == 0){
				typing = true;
			}
		}
		if(equipped[1]){
			if(poemtypehitbox.contains(arg0.getPoint())){
				typing = true;
			}
		}
		if(gamestate == 15){
			if(rockbuttons[0].contains(arg0.getPoint())){
				if(rockcombohelper[0] == 0){
					rockcombo[0] = false;
					rockcombohelper[0]++;
					s1.play(3);
				}

			}
			if(rockbuttons[1].contains(arg0.getPoint())){
				if(rockcombohelper[1] == 0){
					rockcombo[1] = false;
					rockcombohelper[1]++;
					s1.play(3);
				}
				
				
			}
			if(rockbuttons[2].contains(arg0.getPoint())){
				if(rockcombohelper[2] == 0){
					rockcombo[2] = true;
					rockcombohelper[2]++;
					s1.play(3);
				}
				
				
			}
			if(rockbuttons[3].contains(arg0.getPoint())){
				if(rockcombohelper[3] == 0){
					rockcombo[3] = false;
					rockcombohelper[3]++;
					s1.play(3);
				}
				
			}
			if(rockbuttons[4].contains(arg0.getPoint())){
				if(rockcombohelper[4] == 0){
					rockcombo[4] = true;
					rockcombohelper[4]++;
					s1.play(3);
				}
				
			}
			if(rockbuttons[5].contains(arg0.getPoint())){
				if(rockcombohelper[0] == 0){
					rockcombo[0] = true;
					rockcombohelper[0]++;
					s1.play(3);
				}
				
			}
			if(rockbuttons[6].contains(arg0.getPoint())){
				if(rockcombohelper[1] == 0){
					rockcombo[1] = true;
					rockcombohelper[1]++;
					s1.play(3);
				}
			
			}
			if(rockbuttons[7].contains(arg0.getPoint())){
				if(rockcombohelper[2] == 0){
					rockcombo[2] = false;
					rockcombohelper[2]++;
					s1.play(3);
				}
				
			}
			if(rockbuttons[8].contains(arg0.getPoint())){
				if(rockcombohelper[3] == 0){
					rockcombo[3] = true;
					rockcombohelper[3]++;
					s1.play(3);
				}
				
			}
			if(rockbuttons[9].contains(arg0.getPoint())){
				if(rockcombohelper[4] == 0){
					rockcombo[4] = false;
					rockcombohelper[4]++;
					s1.play(3);
				}
				
			}
			if(rockcombo[0] && rockcombo[1] && rockcombo[2] && rockcombo[3] && rockcombo[4]){
				rockcomplete = true;
			}
		}
		
		//below is items equipping
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23) && paper1.contains(arg0.getPoint())){
			if(items[0]){
				if(equippedholder == 0){
					equipped[0] = true;
					equippedholder++;
				}
			}
		}
		else if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)	 && paper2.contains(arg0.getPoint())){
			if(items[1]){
				if(equippedholder == 0){
					equipped[1] = true;
					equippedholder++;
					altartyped = "";
					notetyped = "";
					statuetyped = "";
				}
			}
		}
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)	 && paper3.contains(arg0.getPoint())){
			if(items[2]){
				if(equippedholder == 0){
					equipped[2] = true;
					equippedholder++;
				}
			}
		}
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)	 && paper4.contains(arg0.getPoint())){
			if(items[3]){
				if(equippedholder == 0){
					equipped[3] = true;
					equippedholder++;
				}
			}
		}
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)	 && key.contains(arg0.getPoint())){
			if(items[4]){
				if(equippedholder == 0){
					equipped[4] = true;
					equippedholder++;
				}
			}
		}
		if(((gamestate > 5 && gamestate < 19)	|| gamestate == 23)	 && flute.contains(arg0.getPoint())){
			if(items[5]){
				if(equippedholder == 0){
					equipped[5] = true;
					equippedholder++;
				}
			}
		}
		
		//flute logic (ivory should go 0-4)
		if(gamestate == 12 && equipped[5] == true){
			if(red.contains(arg0.getPoint())){
				if(pressed == 3){
					flutecode[3] = true;
				}
				if(pressed < 5){
					s1.play(5);
				}
				pressed++;
			}
			
			if(orange.contains(arg0.getPoint())){
				if(pressed == 2){
					flutecode[2] = true;
				}
				if(pressed < 5){
					s1.play(6);
				}
				pressed++;
			}
			
			if(yellow.contains(arg0.getPoint())){
				if(pressed == 4){
					flutecode[4] = true;
				}
				if(pressed < 5){
					s1.play(7);
				}
				pressed++;
			}
			
			if(green.contains(arg0.getPoint())){
				if(pressed < 5){
					s1.play(8);
				}
				pressed++;
			}
			
			if(blue.contains(arg0.getPoint())){
				if(pressed < 5){
					s1.play(9);
				}
				pressed++;
			}
			
			if(indigo.contains(arg0.getPoint())){
				if(pressed == 0){
					flutecode[0] = true;
				}
				if(pressed < 10){
					s1.play(10);
				}
				pressed++;
			}
			
			if(violet.contains(arg0.getPoint())){
				if(pressed == 1){
					flutecode[1] = true;
				}
				if(pressed < 5){
					s1.play(11);
				}
				pressed++;
			}
			
			if(flutecode[0] && flutecode[1] && flutecode[2] && flutecode[3] && flutecode[4]){
				flutecomplete = true;
			}
		}
		//constructor twicd
		if(gamestate >= 19 && gamestate < 23 ){
			gamestate = 0;
			i=0;
			f=0;
		
			altartyped = "";
			altartarget = "flora";
			notetyped = "";
			notetarget = "past present future";
			notetarget2 = "past present and future";
			statuetyped = "";
			statuetarget = "elm";
			
			for(int i = 0; i < 6; i++){
				items[i] = false;
			}
			//0 = initial
			//1 = altar
			//2 = tree
			//3 = rock
			//4 = key
			//5 = flute
			items[0] = true;
			items[1] = true;
			
			
			
			notecomplete = false; 
			
			textpage = -1;
			
		
			chestlock[0] = 0;
			chestlock[1] = 0;
			chestlock[2] = 0;
			
			rockcombo[0] = false;
			rockcombo[1] = false;
			rockcombo[2] = false;
			rockcombo[3] = false;
			rockcombo[4] = false;
		
			
			gamestate = 0;
			rand = 0;
			rockcomplete = false;
			chestcomplete = false;
			treeopen = false;
			statuecomplete = false;
			altarcomplete = false;
			flutecomplete = false;
			gamestart = false;
			rock1 = false;
			rock2 = false;
			rock3 = false;
			rock4 = false;
			rock5 = false;
			chest1 = false;
			chest2 = false;
			chest3 = false;
			ped1 = false;
			ped2 = false;
			ped3 = false;
			typing = false;
			inventory = this.addImage("lameassinventory.png");
			rockcloseup = this.addImage("rock.jpg");
			title = this.addImage("titlelogo.png");
			cbg = this.addImage("cbg.png");
			background[0] = this.addImage("bgfront.jpg");
			background[1] = this.addImage("bgright.jpg");
			background[2] = this.addImage("bgback.jpg");
			background[3] = this.addImage("bgleft.jpg");
			timer1 = 20;
			timer2 = 0;
			delay = 30;
			wholescreen = new Rectangle(0,0,1366,720);
			
			for(int i =0; i<6; i++){
				equipped[i] = false;
			}
			equippedholder = 0;
			
		
			pressed = 0;
			for(int i = 0; i<5; i++){
				flutecode[i] = false;
			}
			
		}
		
		else if(gamestate == 22){
			gamestate = 0;
			i=0;
			f=0;
		
			altartyped = "";
			altartarget = "flora";
			notetyped = "";
			notetarget = "past present future";
			notetarget2 = "past present and future";
			statuetyped = "";
			statuetarget = "elm";
			
			for(int i = 0; i < 6; i++){
				items[i] = false;
			}
			//0 = initial
			//1 = altar
			//2 = tree
			//3 = rock
			//4 = key
			//5 = flute
			items[0] = true;
			items[1] = true;
			
			
			
			notecomplete = false; 
			
			textpage = -1;
			
		
			chestlock[0] = 0;
			chestlock[1] = 0;
			chestlock[2] = 0;
			
			rockcombo[0] = false;
			rockcombo[1] = false;
			rockcombo[2] = false;
			rockcombo[3] = false;
			rockcombo[4] = false;
		
			
			gamestate = 0;
			rand = 0;
			rockcomplete = false;
			chestcomplete = false;
			treeopen = false;
			statuecomplete = false;
			altarcomplete = false;
			flutecomplete = false;
			gamestart = false;
			rock1 = false;
			rock2 = false;
			rock3 = false;
			rock4 = false;
			rock5 = false;
			chest1 = false;
			chest2 = false;
			chest3 = false;
			ped1 = false;
			ped2 = false;
			ped3 = false;
			typing = false;
			inventory = this.addImage("lameassinventory.png");
			rockcloseup = this.addImage("rock.jpg");
			title = this.addImage("titlelogo.png");
			cbg = this.addImage("cbg.png");
			background[0] = this.addImage("bgfront.jpg");
			background[1] = this.addImage("bgright.jpg");
			background[2] = this.addImage("bgback.jpg");
			background[3] = this.addImage("bgleft.jpg");
			timer1 = 20;
			timer2 = 0;
			delay = 30;
			wholescreen = new Rectangle(0,0,1366,720);
			
			for(int i =0; i<6; i++){
				equipped[i] = false;
			}
			equippedholder = 0;
			
		
			pressed = 0;
			for(int i = 0; i<5; i++){
				flutecode[i] = false;
			}
			
			
		
		}
		if(statuecomplete){
			if(gamestate == 18 && statueflutehitbox.contains(arg0.getPoint())){
				items[5] = true;
				statuecomplete = false;
				s1.play(4);
			}
		}
		//typing for altar
		if(gamestate == 10 && altartypedhitbox.contains(arg0.getPoint())){
			if(f==0){
				typing = true;	
			}
		}
		if(gamestate == 10 && altartypedhitbox.contains(arg0.getPoint())){
			if(altarcomplete){
				altarcomplete = false;
				items[2] = true;
				s1.play(4);
			}
		}
		
		//hitbox for note in tree
		if(gamestate == 14 && treenotehitbox.contains(arg0.getPoint())){
			items[3] = true;
			s1.play(4);
		}
		
		if(equipped[0]){
			if(textpage < 1){
				textpage++;
			}
		
		}
		
		
	}


	@Override
	public void mouseReleased(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void mouseDragged(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void mouseMoved(MouseEvent arg0) {
		// TODO Auto-generated method stub
		if(gamestate == 10){
			if(altartypedhitbox.contains(arg0.getPoint())){
					typepossibletext[0] = true;
			}
		}
		if(gamestate == 10){
			if(!altartypedhitbox.contains(arg0.getPoint())){
					typepossibletext[0] = false;
			}
		}
		if(gamestate == 18){
			if(dialgatexthitbox.contains(arg0.getPoint())){
					typepossibletext[1] = true;
			}
		}
		if(gamestate == 18){
			if(!dialgatexthitbox.contains(arg0.getPoint())){
					typepossibletext[1] = false;
			}
		}
		if(equipped[1] && !notecomplete){
			if(poemtypehitbox.contains(arg0.getPoint())){
					typepossibletext[2] = true;
			}
		}
		if(equipped[1] && !notecomplete){
			if(!poemtypehitbox.contains(arg0.getPoint())){
					typepossibletext[2] = false;
			}
		}
		if(notecomplete){
			typepossibletext[2] = false;
		}
	}

}
