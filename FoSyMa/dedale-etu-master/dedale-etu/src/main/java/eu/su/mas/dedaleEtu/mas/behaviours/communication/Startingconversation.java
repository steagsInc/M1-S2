package eu.su.mas.dedaleEtu.mas.behaviours.communication;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.SimpleBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.lang.acl.UnreadableException;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;

/**
 * This behaviour is a one Shot.
 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
 * 
 * @author Cédric Herpson
 *
 */
public class Startingconversation extends CustomCommunicationBehaviour{

	private static final long serialVersionUID = 9088209402507795289L;

	private boolean finished=false;

	/**
	 * 
	 * This behaviour is a one Shot.
	 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
	 * @param myagent
	 */
	public Startingconversation(final Agent myagent) {
		super(myagent);

	}


	protected void sendMessage() {
		//1) receive the message
		final MessageTemplate msgTemplate =MessageTemplate.and( MessageTemplate.MatchPerformative(ACLMessage.REQUEST), MessageTemplate.MatchProtocol("Stop"));
		
		final ACLMessage msg = this.myAgent.receive(msgTemplate);
		
		if (msg != null) {		
			System.out.println(this.myAgent.getLocalName()+" <----Stop Request received from "+msg.getSender().getLocalName());
			agent.getExplo().block();
			if( agent.getConversationID(msg.getSender().getLocalName())>=0) {
				
				agent.newConversation(msg.getSender().getLocalName());
				
				ACLMessage answer=new ACLMessage(ACLMessage.CONFIRM);
				answer.setSender(this.myAgent.getAID());
				answer.setProtocol("hasStoped");
				answer.addReceiver(new AID(msg.getSender().getLocalName(),AID.ISLOCALNAME));
				
				this.agent.sendMessage(answer);
				
			}
		}else{
			block();// the behaviour goes to sleep until the arrival of a new message in the agent's Inbox.
		}
	}

	public boolean done() {
		return finished;
	}

}