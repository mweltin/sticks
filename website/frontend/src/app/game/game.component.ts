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

  // Initialzise all properties to empty values

  // [[ai left, ai right][human left, human right]] this convention comes from the python side
  state: number[][] = [[0,0], [0,0]];

  // this holds the value of the active player either 'human' or 'qlearning'
  whoseTurnIsIt: string = '';

  // These are the inputs to the player component and by extension the hand component
  QLFingers: number = 0;
  QRFingers: number = 0;
  HLFingers: number = 0;
  HRFingers: number = 0;

  // Action queue is an object that gets passed to the web backend and defines what a the
  // desired action is.  The swap action takes place client site.  Hence this object is only
  // sent to the server when the human player is touching the hand of the qlearning player.
  // the human.activeHand is the hand the human will use to touch the qleaning's activeHand.
  actionQueue: ActionQueue = {
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

  constructor( private turnSrv: TurnService) {

  }

  ngOnInit(): void {
    // now that we are an actual component set the initial state.
    this.whoseTurnIsIt = '';
    this.QLFingers = 1;
    this.QRFingers = 1;
    this.HLFingers = 1;
    this.HRFingers = 1;
  }

  aiTakeTurn(){
    this.actionQueue.activePlayer = this.whoseTurnIsIt;
    this.actionQueue.human.playerState = [this.HLFingers, this.HRFingers];
    this.actionQueue.qlearning.playerState = [this.QLFingers, this.QRFingers];
      this.turnSrv.takeATurn(this.actionQueue).subscribe(
        (res: any) => {
          this.processTurnSrvResults(res);
        },
        (error: any) =>
          console.log(error)
      );
  }

  playerActionHandler( action:PlayerAction )
  {
    // click all you want we are not doing anything until it is your turn.
    if(this.whoseTurnIsIt == 'qlearning' || this.whoseTurnIsIt == ''){
      return;
    }

    // you can click hands in any order and even change your mind (sort of).
    if(action.playerType == 'qlearning'){
      this.actionQueue.qlearning = action;
    }
    if(action.playerType == 'human'){
      this.actionQueue.human = action;
    }

    // As soon as both human and qlearning actions are set we submit to the backend.
    if( this.actionQueue.human.playerType != '' && this.actionQueue.qlearning.playerType != '' ){
      this.actionQueue.activePlayer = this.whoseTurnIsIt;
      this.turnSrv.takeATurn(this.actionQueue).subscribe(
        (res: any) => {
          this.processTurnSrvResults(res);
        },
        (error: any) =>
          console.log(error)
      );
    }
  }

  processTurnSrvResults(res: any){
    console.log("turn service returned an object " + JSON.stringify(res));
    this.turnSrv.updatePlayMessage(JSON.stringify(res))
    this.updateHands(res);
    this.clearActionQueue();
    this.changeActivePlayer();
    if(res.hasWinner == true){
      alert(this.whoseTurnIsIt +   " has won!" + "Refresh browser to play again. ");
    }
  }

  // When the app loads two buttons
  whoGoesFirst(player : string){
    if( player == 'human' ){
      this.whoseTurnIsIt = 'human';
    }
    if (player == 'qlearning'){
      this.whoseTurnIsIt = 'qlearning';

      //pause for a sec to make it look like the AI is thinking
      setTimeout(() => {
        this.aiTakeTurn();
      }, 1000);
    }
  }

  // the backend is stateless so it's easier to just do the swap client site.
  swapActionHandler(message:any){
    this.turnSrv.updatePlayMessage("took a swap")
    console.log(message.playerType + "  " + message.value);
    if(message.playerType = 'human'){
      this.HLFingers = message.value;
      this.HRFingers = message.value;
    } else {
      this.QLFingers = message.value;
      this.QRFingers = message.value;
    }
    this.changeActivePlayer();
  }

  // sets the active player.  When the active player switches to the qlearning AI it also
  // takes it's turn.
  changeActivePlayer(){
    if(this.whoseTurnIsIt == 'human')
    {
      this.whoseTurnIsIt = 'qlearning';
      setTimeout(() => {
        this.aiTakeTurn();
      }, 1000);
    } else {
      this.whoseTurnIsIt = 'human';
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
    this.HLFingers = res.state[1][0];
    this.HRFingers = res.state[1][1];
    this.QLFingers = res.state[0][0];
    this.QRFingers = res.state[0][1];
  }
}
