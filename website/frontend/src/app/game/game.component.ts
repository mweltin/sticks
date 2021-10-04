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
  event: PlayerAction = { playerState: [], playerType:'',activeHand:'' };
  actionQueue: ActionQueue =     {
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

  playerActionHandler( playerAction:PlayerAction )
  {
    if(playerAction.playerType == 'qlearning'){
      this.actionQueue.qlearning = playerAction;
    }
    if(playerAction.playerType == 'human'){
      this.actionQueue.human = playerAction;
    }
    if( this.actionQueue.human.playerType != '' && this.actionQueue.qlearning.playerType != '' ){
      this.turnSrv.takeATurn(this.actionQueue).subscribe(
        (res: any) => {
          console.log("turn service returned an object " + res);
          this.changeActivePlayer();
          this.actionQueue = {
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
    } else {
      this.whoesTurnIsIt = 'human';
    }
  }

}
