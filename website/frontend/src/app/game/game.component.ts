import { Component, OnInit } from '@angular/core';
import { TurnService } from '../turn.service';
import { ActionQueue } from '../action-queue';
import { PlayerAction } from '../player-action';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  // [[human left, human right][qlearning left, qlearning right]]
  state: number[][] = [[1,1], [1,1]];
  whoesTurnIsIt: string = '';
  QLFingers: number = 1;
  QRFingers: number = 1;
  HLFingers: number = 1;
  HRFingers: number = 1;
  message: string = '';
  actionQueue: ActionQueue =     {
    activePlayer: '',
    human:  {    
      playerState: [],
      activeHand: '',
      playerType: ''
    },
    qlearning: {    
      playerState: [],  
      activeHand: '',
      playerType: ''
    }
  };;

  constructor( private turnSrv: TurnService) { }

  ngOnInit(): void {
    this.whoesTurnIsIt = '';
  }

  aiTakeTurn(){
    this.actionQueue.activePlayer = this.whoesTurnIsIt;
    this.actionQueue.human.playerState = [this.HLFingers, this.HRFingers];
    this.actionQueue.qlearning.playerState = [this.QLFingers, this.QRFingers];
      this.turnSrv.takeATurn(this.actionQueue).subscribe(
        (res: any) => {
          console.log("turn service returned an object " + res);
          this.changeActivePlayer();
          this.updateHands(res);
          this.clearActionQueue();
        },
        (error: any) => 
          console.log(error)
      );
  }

  playerActionHandler( action:PlayerAction )
  {
    if(this.whoesTurnIsIt == 'qlearning'){
      return;
    }
    if(action.playerType == 'qlearning'){
      this.actionQueue.qlearning = action;
    }
    if(action.playerType == 'human'){
      this.actionQueue.human = action;
    }
    if( this.actionQueue.human.playerType != '' && this.actionQueue.qlearning.playerType != '' ){
      this.actionQueue.activePlayer = this.whoesTurnIsIt;
      this.turnSrv.takeATurn(this.actionQueue).subscribe(
        (res: any) => {
          console.log("turn service returned an object " + res);
          this.changeActivePlayer();
          this.updateHands(res);
          this.clearActionQueue();
        },
        (error: any) => 
          console.log(error)
      );
    }
  }

  whoGoesFirst(player : string){
    if( player == 'human' ){
      this.whoesTurnIsIt = 'human';
    } 
    if (player == 'qlearning'){
      this.whoesTurnIsIt = 'qlearning';
      //@todo make UI elements not clickable 
      //pause for a sec to make it look like the AI is thinking
      setTimeout(() => {
        this.aiTakeTurn();
      }, 1000);
    }
  }

  swapActionHandler(message: string){
    console.log(message);
    this.changeActivePlayer();
  }

  changeActivePlayer(){
    if(this.whoesTurnIsIt == 'human')
    {
      this.whoesTurnIsIt = 'qlearning';
      setTimeout(() => {
        this.aiTakeTurn();
      }, 1000);
    } else {
      this.whoesTurnIsIt = 'human';
    }
  }

  clearActionQueue(){
    this.actionQueue = {
      activePlayer: '',
      human:  {    
        playerState: [],
        activeHand: '',
        playerType: ''
      },
      qlearning: {    
        playerState: [],  
        activeHand: '',
        playerType: ''
      }
    };
  }

  updateHands(res: any){
    this.HLFingers = res.state[0][0];
    this.HRFingers = res.state[0][1];
    this.QLFingers = res.state[1][0];
    this.QRFingers = res.state[1][1];
  }
}
