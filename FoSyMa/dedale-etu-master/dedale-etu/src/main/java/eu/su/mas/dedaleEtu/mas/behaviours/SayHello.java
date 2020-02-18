package eu.su.mas.dedaleEtu.mas.behaviours;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;

import com.sun.xml.internal.bind.v2.runtime.reflect.opt.TransducedAccessor_field_Short;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;
import jade.lang.acl.ACLMessage;

/**
 * This example behaviour try to send a hello message (every 3s maximum) to agents Collect2 Collect1
 * @author hc
 *
 */
public class SayHello extends TickerBehaviour{

	/**
	 * 
	 */
	private static final long serialVersionUID = -2058134622078521998L;

	/**
	 * An agent tries to contact its friend and to give him its current position
	 * @param myagent the agent who posses the behaviour
	 *  
	 */
	public SayHello (final Agent myagent) {
		super(myagent, 3000);
		//super(myagent);
	}

	@Override
	public void onTick() {
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();

		//A message is defined by : a performative, a sender, a set of receivers, (a protocol),(a content (and/or contentOBject))
		ACLMessage msg=new ACLMessage(ACLMessage.INFORM);
		msg.setSender(this.myAgent.getAID());
		msg.setProtocol("UselessProtocol");

		if (myPosition!=""){
			
			HashMap<String,Object> truc = new HashMap();
			
			truc.put("open", ((ExploreSoloAgent)this.myAgent).getSolo().getOpenNodes());
			truc.put("close", ((ExploreSoloAgent)this.myAgent).getSolo().getClosedNodes());
				
			
			System.out.println("Agent "+this.myAgent.getLocalName()+ " is trying to reach its friends");
			msg.setContent("Hello World, I'm at "+myPosition);
			try {
				msg.setContentObject(truc);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			msg.addReceiver(new AID("Explo1",AID.ISLOCALNAME));
			msg.addReceiver(new AID("Explo2",AID.ISLOCALNAME));

			//Mandatory to use this method (it takes into account the environment to decide if someone is reachable or not)
			((AbstractDedaleAgent)this.myAgent).sendMessage(msg);
		}
	}
}