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
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.ExploDuoBehaviour;

/**
 * This behaviour is a one Shot.
 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
 * 
 * @author Cédric Herpson
 *
 */
public class ReceiveMap extends CustomCommunicationBehaviour{

	private static final long serialVersionUID = 9088209402507795289L;

	private boolean finished=false;

	/**
	 * 
	 * This behaviour is a one Shot.
	 * It receives a message tagged with an inform performative, print the content in the console and destroy itlself
	 * @param myagent
	 */
	public ReceiveMap(final Agent myagent) {
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
				
				if(agent.getExplo() instanceof ExploDuoBehaviour) {
					agent.getMapping().setObjectives((List<String>)truc.get("objectives"));
					((ExploDuoBehaviour)agent.getExplo()).setRdv(((AbstractDedaleAgent)this.myAgent).getCurrentPosition());
				}
				
				ACLMessage answer=new ACLMessage(ACLMessage.CONFIRM);
				answer.setSender(this.myAgent.getAID());
				answer.setProtocol("MapReceived");
				answer.addReceiver(new AID(msg.getSender().getLocalName(),AID.ISLOCALNAME));
				
				this.agent.sendMessage(answer);
				
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