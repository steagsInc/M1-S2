package eu.su.mas.dedaleEtu.mas.agents.dummies;

import java.util.ArrayList;
import java.util.List;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedale.mas.agent.behaviours.startMyBehaviours;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.AskStop;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.ReceiveMessageBehaviour;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.SendMap;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.Theonewhostops;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.ExploSoloBehaviour;
import eu.su.mas.dedaleEtu.mas.knowledge.MapRepresentation;
import eu.su.mas.dedaleEtu.mas.knowledge.YellowPage;
import jade.core.behaviours.Behaviour;

/**
 * <pre>
 * ExploreSolo agent. 
 * It explore the map using a DFS algorithm.
 * It stops when all nodes have been visited.
 *  </pre>
 *  
 * @author hc
 *
 */

public class ExploreSoloAgent extends AbstractDedaleAgent {

	private static final long serialVersionUID = -6431752665590433727L;
	private MapRepresentation myMap;
	private ExploSoloBehaviour solo;
	private AskStop stop;
	private YellowPage yellowpage;
	private int conversationID = 0;
	
	private final int COOLDOWN =-5;
	
	/**
	 * This method is automatically called when "agent".start() is executed.
	 * Consider that Agent is launched for the first time. 
	 * 			1) set the agent attributes 
	 *	 		2) add the behaviours
	 *          
	 */
	
	protected void setup(){

		super.setup();
		

		List<Behaviour> lb=new ArrayList<Behaviour>();
		
		
		/************************************************
		 * 
		 * ADD the behaviours of the Dummy Moving Agent
		 * 
		 ************************************************/
		
		this.solo = new ExploSoloBehaviour(this,this.myMap);
		this.stop = new AskStop(this);
		this.yellowpage = YellowPage.getinstance();
		this.yellowpage.register(this);
		lb.add(solo);
		lb.add(new SendMap(this));
		lb.add(stop);
		lb.add(new Theonewhostops(this));
		lb.add(new ReceiveMessageBehaviour(this));
		/***
		 * MANDATORY TO ALLOW YOUR AGENT TO BE DEPLOYED CORRECTLY
		 */
		
		
		addBehaviour(new startMyBehaviours(this,lb));
		
		System.out.println("the  agent "+this.getLocalName()+ " is started");

	}


	public ExploSoloBehaviour getSolo() {
		return solo;
	}


	public AskStop getStop() {
		return stop;
	}


	public YellowPage getYellowpage() {
		return yellowpage;
	}


	public int getConversationID() {
		if (this.conversationID<0) this.conversationID++;
		return this.conversationID;
	}
	
	public int newConversationID() {
		this.conversationID = (int) (Math.random() * ( 0 - 99999 ));
		
		return this.conversationID;
	}
	
	public void newCoolDown() {
		this.conversationID=COOLDOWN;
	}


	public void setConversationID(int conversationID) {
		this.conversationID = conversationID;
	}
}
