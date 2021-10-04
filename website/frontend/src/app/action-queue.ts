import { PlayerAction } from "./player-action";
export interface ActionQueue {
    human: PlayerAction;
    qlearning: PlayerAction;
}
