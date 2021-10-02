import { Component, OnInit } from '@angular/core';

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

  constructor() { 

  }

  ngOnInit(): void {
    this.whoesTurnIsIt = 'human';
  }

  playerActionHandler( playerAction:object )
  {
    console.log("why does thsi work "+ playerAction);
    this.QLFingers = Math.round( Math.random() *100) % 5;
    this.QRFingers = Math.round( Math.random() *100) % 5;
    this.HLFingers = Math.round( Math.random() *100) % 5;
    this.HRFingers = Math.round( Math.random() *100) % 5;
  }

}
