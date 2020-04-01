package eu.su.mas.dedaleEtu.mas.behaviours.communication;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

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
public class ReceiveMessageBehaviour extends CustomCommunicationBehaviour{

	private static final long serialVersionUID = 9088209402507795289L;

	private boolean finished=false;

	/**
	 * 
	 * This behaviour is a one Shot.
	 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
	 * @param myagent
	 */
	public ReceiveMessageBehaviour(final Agent myagent) {
		super(myagent);

	}


	protected void getAnswer() {
		//1) receive the message
		final MessageTemplate msgTemplate =MessageTemplate.and( MessageTemplate.MatchPerformative(ACLMessage.INFORM), MessageTemplate.MatchProtocol("map"));

		final ACLMessage msg = this.myAgent.receive(msgTemplate);
		
		if (msg != null) {		
			
			System.out.println(this.myAgent.getLocalName()+"<----Result received from "+msg.getSender().getLocalName());
			try {
				HashMap<String,Object> truc = (HashMap<String, Object>) msg.getContentObject();	
				agent.getMapping().mergeMap((List<String>)truc.get("open"),(Set<String>)truc.get("closed"),(List<String>)truc.get("edges"));
				agent.getExplo().restart();
				
				agent.endConversation(msg.getSender().getLocalName());
				
			} catch (UnreadableException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}else{
			block();// the behaviour goes to sleep until the arrival of a new message in the agent's Inbox.
		}
	}

	public boolean done() {
		return finished;
	}

}