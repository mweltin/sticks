import { PlayerAction } from "./player-action";
export interface ActionQueue {
    activePlayer: string;
    human: PlayerAction;
    qlearning: PlayerAction;
}
