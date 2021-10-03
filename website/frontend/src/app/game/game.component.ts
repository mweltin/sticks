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
  QLFingers: number = 1;
  QRFingers: number = 1;
  HLFingers: number = 1;
  HRFingers: number = 1;

  constructor( private turnSrv: TurnService) { }

  ngOnInit(): void {
    this.whoesTurnIsIt = 'human';
  }

  playerActionHandler( playerAction:object )
  {
    this.turnSrv.takeATurn(playerAction).subscribe(
      (res: any) => {
        console.log("turn service returned an object " + res)
      },
      (error: any) => 
      {
        console.log(error)
      }
    );
  }


}
