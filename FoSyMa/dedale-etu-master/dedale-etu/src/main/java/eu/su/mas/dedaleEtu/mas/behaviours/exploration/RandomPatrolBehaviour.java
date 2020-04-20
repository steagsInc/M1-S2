package eu.su.mas.dedaleEtu.mas.behaviours.exploration;

import java.io.IOException;
import java.util.List;
import java.util.Random;

import dataStructures.tuple.Couple;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.behaviours.knowledge.MappingBehaviour;
import eu.su.mas.dedaleEtu.mas.knowledge.MapRepresentation;
import jade.core.behaviours.TickerBehaviour;

/**************************************
 * 
 * 
 * 				BEHAVIOUR RandomWalk : Illustrates how an agent can interact with, and move in, the environment
 * 
 * 
 **************************************/


public class RandomPatrolBehaviour extends CustomExplorationBehaviour{
	
	/**
	 * When an agent choose to move
	 *  
	 */
	private static final long serialVersionUID = 9088209402507795289L;
	
	private MappingBehaviour mapping;

	public RandomPatrolBehaviour (final AbstractDedaleAgent myagent,MappingBehaviour mapping) {
		super(myagent);
		this.mapping = mapping;
	}

	@Override
	public void action() {
		//Example to retrieve the current position
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();
		if (myPosition!=null){
			//List of observable from the agent's current position
			List<Couple<String,List<Couple<Observation,Integer>>>> lobs=((AbstractDedaleAgent)this.myAgent).observe();//myPosition
			System.out.println(this.myAgent.getLocalName()+" -- list of observables: "+lobs);

			String nextMove = null;
			for(Couple<String,List<Couple<Observation,Integer>>> po:lobs){
				for(Couple<Observation,Integer> o:po.getRight()) {
					if(o.getLeft().equals(Observation.STENCH)) {
						nextMove = po.getLeft();
						break;
					}
				}
				if(nextMove!=null) break;
			}

			if(nextMove!=null) {
				if(this.mapping.getMyMap().getShortestPath(myPosition, nextMove).isEmpty()) {
					((AbstractDedaleAgent)this.myAgent).moveTo(nextMove);
				}else {
					((AbstractDedaleAgent)this.myAgent).moveTo(this.mapping.getMyMap().getShortestPath(myPosition, nextMove).get(0));
				}
			}else {
				Random r= new Random();
				int moveId=1+r.nextInt(lobs.size()-1);
				((AbstractDedaleAgent)this.myAgent).moveTo(lobs.get(moveId).getLeft());
			}
			
		}

	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}

}