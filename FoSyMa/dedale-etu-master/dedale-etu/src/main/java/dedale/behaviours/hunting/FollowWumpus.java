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


public class FollowWumpus extends CustomExplorationBehaviour{
	
	/**
	 * When an agent choose to move
	 *  
	 */
	private static final long serialVersionUID = 9088209402507795289L;
	
	private MappingBehaviour mapping;
	
	private int lost = 5;

	public FollowWumpus (final AbstractDedaleAgent myagent,MappingBehaviour mapping) {
		super(myagent);
		this.mapping = mapping;
		this.lost = 5;
	}

	@Override
	public void action() {
		//Example to retrieve the current position
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();
		if (myPosition!=null){
			
			try {
				this.myAgent.doWait(500);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			
			System.out.println("hunt");
			
			List<String> stenchs = ((CustomAgent)this.myAgent).getStenchs();
			
			stenchs.removeAll(this.mapping.getAgentsPos());
			
			//System.out.println(stenchs);
			
			//System.out.println(this.myAgent.getLocalName());
			
			String nextMove = null;
			
			if(!stenchs.isEmpty()) nextMove = stenchs.get(0);

			if(nextMove!=null) {
				String nextPos = this.mapping.getPath(myPosition, nextMove);
				if(nextPos!="") ((AbstractDedaleAgent)this.myAgent).moveTo(nextPos);
			}else{
				
				lost--;
			}
			
		}

	}

	@Override
    public int onEnd() {
		if(lost<=0) {
			System.out.println("lost him");
			return 1;
		}
        return 0;
    }

}