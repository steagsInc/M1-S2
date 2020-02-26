package eu.su.mas.dedaleEtu.mas.behaviours;

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
public class Theonewhostops extends SimpleBehaviour{

	private static final long serialVersionUID = 9088209402507795289L;

	private boolean finished=false;

	/**
	 * 
	 * This behaviour is a one Shot.
	 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
	 * @param myagent
	 */
	public Theonewhostops(final Agent myagent) {
		super(myagent);

	}


	public void action() {
		//1) receive the message
		final MessageTemplate msgTemplate = MessageTemplate.MatchPerformative(ACLMessage.REQUEST);
		
		final ACLMessage msg = this.myAgent.receive(msgTemplate);
		
		if (msg != null) {		
			System.out.println(this.myAgent.getLocalName()+"<----Request received from "+msg.getSender().getLocalName());
			((ExploreSoloAgent)this.myAgent).getSolo().block();
			
			ACLMessage msg1=new ACLMessage(ACLMessage.CONFIRM);
			msg1.setSender(this.myAgent.getAID());
			msg1.setProtocol("i have stoped");
			msg1.addReceiver(new AID(msg.getSender().getLocalName(),AID.ISLOCALNAME));
			
		}else{
			block();// the behaviour goes to sleep until the arrival of a new message in the agent's Inbox.
		}
	}

	public boolean done() {
		return finished;
	}

}