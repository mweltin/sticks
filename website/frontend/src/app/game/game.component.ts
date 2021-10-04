import { Component, OnInit } from '@angular/core';
import { TurnService } from '../turn.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  // [[human left, human right][qlearning left, qlearning right]]
  state: number[][] = [[1,1], [1,1]];
  whoesTurnIsIt: string = '';
  actionQueue: object[] = [];
  QLFingers: number = 1;
  QRFingers: number = 1;
  HLFingers: number = 1;
  HRFingers: number = 1;
  message: string = '';

  constructor( private turnSrv: TurnService) { }

  ngOnInit(): void {
    this.whoesTurnIsIt = '';
  }

  playerActionHandler( playerAction:object )
  {
    this.actionQueue.push(playerAction);
    if( this.actionQueue.length == 2 ){
      this.actionQueue.push({'activePlayer': this.whoesTurnIsIt});
      this.turnSrv.takeATurn(playerAction).subscribe(
        (res: any) => {
          console.log("turn service returned an object " + res);
          this.changeActivePlayer();
          this.actionQueue = [];
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
    this.actionQueue = [];
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
