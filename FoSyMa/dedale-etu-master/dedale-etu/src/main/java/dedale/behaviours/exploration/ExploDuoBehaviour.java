package dedale.behaviours.exploration;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import dataStructures.tuple.Couple;
import dedale.agents.CustomAgent;
import dedale.agents.ExploreSoloAgent;
import dedale.behaviours.knowledge.MappingBehaviour;
import dedale.knowledge.MapRepresentation;
import dedale.knowledge.MapRepresentation.MapAttribute;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.SimpleBehaviour;


/**
 * This behaviour allows an agent to explore the environment and learn the associated topological map.
 * The algorithm is a pseudo - DFS computationally consuming because its not optimised at all.</br>
 * 
 * When all the nodes around him are visited, the agent randomly select an open node and go there to restart its dfs.</br> 
 * This (non optimal) behaviour is done until all nodes are explored. </br> 
 * 
 * Warning, this behaviour does not save the content of visited nodes, only the topology.</br> 
 * Warning, this behaviour is a solo exploration and does not take into account the presence of other agents (or well) and indefinitely tries to reach its target node
 * @author hc
 *
 */
public class ExploDuoBehaviour extends CustomExplorationBehaviour {

	private static final long serialVersionUID = 8567689712496787661L;

	private boolean finished = false;

	private MappingBehaviour mapping;
	
	private String rdv = null;

	public ExploDuoBehaviour(final AbstractDedaleAgent myagent, MappingBehaviour mapping) {
		super(myagent);
		this.mapping=mapping;
	}

	@Override
	public void action() {

		//0) Retrieve the current position
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();
	
		if (myPosition!=null){

			try {
				this.myAgent.doWait(500);
			} catch (Exception e) {
				e.printStackTrace();
			}

			System.out.println("explo");
			String nextNode=this.mapping.getNextObjectif(myPosition);
			
			System.out.println(nextNode);
			
			if (nextNode=="") {
				if(this.rdv!=null && this.rdv != myPosition) {
					nextNode=this.mapping.getPath(myPosition, this.rdv);
					System.out.println("rdv");
					((AbstractDedaleAgent)this.myAgent).moveTo(nextNode);
				}
				else if(this.mapping.getOpenNodes().isEmpty()) {
					finished = true;
				}
			} else if(nextNode=="" && rdv=="") {
				finished = true;
			}else {
				((AbstractDedaleAgent)this.myAgent).moveTo(nextNode);
			}
		}

	}

	@Override
    public int onEnd() {
        return 0;
    }
	
	public void setRdv(String rdv) {
		this.rdv = rdv;
	}
}
