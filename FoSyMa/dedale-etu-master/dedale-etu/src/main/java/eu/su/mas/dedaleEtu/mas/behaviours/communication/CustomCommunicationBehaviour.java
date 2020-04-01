package eu.su.mas.dedaleEtu.mas.behaviours.communication;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.CustomAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;
import jade.core.behaviours.TickerBehaviour;
import jade.lang.acl.ACLMessage;

/**
 * This example behaviour try to send a hello message (every 3s maximum) to agents Collect2 Collect1
 * @author hc
 *
 */
public class CustomCommunicationBehaviour extends SimpleBehaviour{

	/**
	 * 
	 */
	private static final long serialVersionUID = -2058134622078521998L;

	/**
	 * An agent tries to contact its friend and to give him its current position
	 * @param myagent the agent who posses the behaviour
	 *  
	 */
	private String lastPos;
	protected CustomAgent agent;
	
	public CustomCommunicationBehaviour (final Agent myagent) {
		super(myagent);
		this.lastPos="";
		this.agent = (CustomAgent)myagent;
	}

	protected void sendMessage() {
		
	}
	
	protected void getAnswer() {
		
	}
	
	@Override
	public void action() {
		sendMessage();
		getAnswer();
	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}
}