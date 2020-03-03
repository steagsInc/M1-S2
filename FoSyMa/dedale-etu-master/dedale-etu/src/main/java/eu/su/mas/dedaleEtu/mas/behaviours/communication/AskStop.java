package eu.su.mas.dedaleEtu.mas.behaviours.communication;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import com.sun.xml.internal.bind.v2.runtime.reflect.opt.TransducedAccessor_field_Short;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
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
public class AskStop extends SimpleBehaviour{

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
	
	public AskStop (final Agent myagent) {
		super(myagent);
		this.lastPos="";
	}

	@Override
	public void action() {
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();

		//A message is defined by : a performative, a sender, a set of receivers, (a protocol),(a content (and/or contentOBject))
		ACLMessage msg=new ACLMessage(ACLMessage.REQUEST);
		msg.setSender(this.myAgent.getAID());
		msg.setProtocol("Stop");
		
		ExploreSoloAgent agent=(ExploreSoloAgent) this.myAgent;

		if (myPosition!="" && myPosition!=this.lastPos && agent.getConversationID()==0){
			
			//System.out.println("Agent "+this.myAgent.getLocalName()+ " is trying to reach its friends");
			msg.setContent("Hello World, I'm at "+myPosition);

			List<AbstractDedaleAgent> agents =((ExploreSoloAgent)this.myAgent).getYellowpage().getOtherAgents((AbstractDedaleAgent) this.myAgent);
			
			for(AbstractDedaleAgent a:agents) {
				msg.addReceiver(new AID(a.getLocalName(),AID.ISLOCALNAME));
			}

			//Mandatory to use this method (it takes into account the environment to decide if someone is reachable or not)
			((AbstractDedaleAgent)this.myAgent).sendMessage(msg);
			this.lastPos=myPosition;
		}
	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}
}