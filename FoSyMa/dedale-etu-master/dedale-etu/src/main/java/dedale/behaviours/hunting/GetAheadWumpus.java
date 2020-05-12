package dedale.behaviours.hunting;

import java.io.IOException;
import java.util.List;
import java.util.Random;

import dataStructures.tuple.Couple;
import dedale.agents.CustomAgent;
import dedale.behaviours.exploration.CustomExplorationBehaviour;
import dedale.behaviours.knowledge.MappingBehaviour;
import dedale.knowledge.MapRepresentation;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import jade.core.behaviours.TickerBehaviour;

/**************************************
 * 
 * 
 * 				BEHAVIOUR RandomWalk : Illustrates how an agent can interact with, and move in, the environment
 * 
 * 
 **************************************/


public class GetAheadWumpus extends CustomExplorationBehaviour{
	
	/**
	 * When an agent choose to move
	 *  
	 */
	private static final long serialVersionUID = 9088209402507795289L;
	
	private MappingBehaviour mapping;

	public GetAheadWumpus (final AbstractDedaleAgent myagent,MappingBehaviour mapping) {
		super(myagent);
		this.mapping = mapping;
	}

	@Override
	public void action() {
		//Example to retrieve the current position
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();
		if (myPosition!=null){
			
			System.out.println("scout "+this.myAgent.getLocalName());
			System.out.println(this.mapping.getWumpusPos());
			
			String nextPos = this.mapping.getPath(myPosition, this.mapping.getWumpusPos());
			
			if(nextPos!="") ((AbstractDedaleAgent)this.myAgent).moveTo(nextPos);
			else {
				System.out.println(this.mapping.getHunterName());
				System.out.println(this.mapping.getAgentPos(this.mapping.getHunterName()));
				nextPos = this.mapping.getPath(myPosition, this.mapping.getAgentPos(this.mapping.getHunterName()));
				if(nextPos!="") ((AbstractDedaleAgent)this.myAgent).moveTo(nextPos);
			}
			
			
		}

	}

	@Override
    public int onEnd() {
        return 0;
    }

}