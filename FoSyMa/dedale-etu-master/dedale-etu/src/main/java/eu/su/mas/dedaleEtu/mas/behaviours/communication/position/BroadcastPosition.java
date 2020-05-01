package eu.su.mas.dedaleEtu.mas.behaviours.communication.position;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.CustomCommunicationBehaviour;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;
import jade.core.behaviours.TickerBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

/**
 * This example behaviour try to send a hello message (every 3s maximum) to agents Collect2 Collect1
 * @author hc
 *
 */
public class BroadcastPosition extends CustomCommunicationBehaviour{

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
	
	private boolean finished = false;
	
	public BroadcastPosition (final Agent myagent) {
		super(myagent);
		this.lastPos="";
	}

	protected void sendMessage() {
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();

		if (myPosition!="" && myPosition!=this.lastPos){
			
			try {
				this.myAgent.doWait(200);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			//System.out.println("Agent "+this.myAgent.getLocalName()+ " is trying to reach its friends");

			List<String> agents =this.agent.getYellowpage().getOtherAgents(this.agent);
			
			ACLMessage msg=new ACLMessage(ACLMessage.INFORM);
			msg.setSender(this.myAgent.getAID());
			msg.setProtocol("Pos");
			msg.setContent(myPosition);
			
			for(String a:agents) {
				if(this.agent.getConversationID(a)>=0) {
					msg.addReceiver(new AID(a,AID.ISLOCALNAME));
				}
			}

			//Mandatory to use this method (it takes into account the environment to decide if someone is reachable or not)
			this.agent.sendMessage(msg);
			this.lastPos=myPosition;
			
		}
		
		if(this.agent.getYellowpage().getOtherAgents(this.agent).isEmpty()) {
			//ne spam pas s'il est tout seul
			finished = true;
		}
	}
	
	protected void getAnswer() {
		
		final MessageTemplate msgTemplate =MessageTemplate.and( MessageTemplate.MatchPerformative(ACLMessage.CONFIRM), MessageTemplate.MatchProtocol("hasStoped"));

		final ACLMessage msg = this.myAgent.receive(msgTemplate);
		if (msg != null) {
			
			agent.newConversation(msg.getSender().getLocalName());
			agent.getExplo().block();
			System.out.println("confirmation");
			
		}
	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return finished;
	}
}