package eu.su.mas.dedaleEtu.mas.agents.dummies;

import java.util.ArrayList;
import java.util.List;

import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedale.mas.agent.behaviours.startMyBehaviours;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.AskStop;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.ReceiveMap;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.SendMap;
import eu.su.mas.dedaleEtu.mas.behaviours.communication.Startingconversation;
import eu.su.mas.dedaleEtu.mas.behaviours.exploration.ExploDuoBehaviour;
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

public class ExploreDuoAgent extends CustomAgent {

	private static final long serialVersionUID = -6431752455590433727L;
	
	protected void setup(){

		super.setup();
		
		this.explo = new ExploDuoBehaviour(this,this.mapping);
		lb.add(this.explo);
		
		addBehaviour(new startMyBehaviours(this,lb));
		
		System.out.println("the  agent "+this.getLocalName()+ " is started");

	}
}
