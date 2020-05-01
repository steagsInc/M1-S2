package eu.su.mas.dedaleEtu.mas.behaviours.communication;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.ExploDuoBehaviour;
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
public class SendMap extends CustomCommunicationBehaviour{

	/**
	 * 
	 */
	private static final long serialVersionUID = -2058134622078521998L;

	/**
	 * An agent tries to contact its friend and to give him its current position
	 * @param myagent the agent who posses the behaviour
	 *  
	 */
	public SendMap (final Agent myagent) {
		super(myagent);
	}

	protected void sendMessage() {
		
		List<String> activeConversations = this.agent.getActiveConversations();
		
		if (!activeConversations.isEmpty()) {
			
			try {
				this.myAgent.doWait(100);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			ACLMessage msg=new ACLMessage(ACLMessage.INFORM);
			msg.setSender(this.myAgent.getAID());
			msg.setProtocol("map");
			
			HashMap<String,Object> truc = new HashMap();
			
			truc.put("open", agent.getMapping().getOpenNodes());
			truc.put("closed", agent.getMapping().getClosedNodes());
			truc.put("edges", agent.getMapping().getEdges());
			if(agent.getExplo() instanceof ExploDuoBehaviour) truc.put("objectives", agent.getMapping().setupObjectives());
				
			//System.out.println("Agent "+this.myAgent.getLocalName()+ " is trying to send a map");
			
			try {
				msg.setContentObject(truc);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			for(String a:activeConversations) {
				msg.addReceiver(new AID(a,AID.ISLOCALNAME));
			}

			this.agent.sendMessage(msg);
			
		}
	}
	
	protected void getAnswer() {
		//1) receive the message
		final MessageTemplate msgTemplate =MessageTemplate.and( MessageTemplate.MatchPerformative(ACLMessage.CONFIRM), MessageTemplate.MatchProtocol("MapReceived"));

		final ACLMessage msg = this.myAgent.receive(msgTemplate);
		
		if (msg != null) {
			
			if(agent.getExplo() instanceof ExploDuoBehaviour) ((ExploDuoBehaviour)agent.getExplo()).setRdv(((AbstractDedaleAgent)this.myAgent).getCurrentPosition());
			
			agent.getExplo().restart();
			
			agent.endConversation(msg.getSender().getLocalName());
			
			System.out.println("Map confirmed");
			
		}
		
	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}
}