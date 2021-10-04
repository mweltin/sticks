import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges, SimpleChange  } from '@angular/core';
import { PlayerAction } from '../player-action';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

  @Input()
  playerType: string = '';
  
  @Input()
  LFingers: number = 1;

  @Input()
  RFingers: number = 1;

  @Output() 
  playerAction: EventEmitter<Object> = new EventEmitter();

  @Output() 
  swapAction: EventEmitter<Object> = new EventEmitter();

  send:PlayerAction =  { 
    playerType: '', 
    playerState: [],
    activeHand: ''
  };

  constructor() { }

  ngOnInit(): void {
    
  }

  swap() {
    this.swapAction.emit("perform swap action for " + this.playerType +"." );
  }

  handClickedHandler(hand: string) {
      this.send = { 
        playerType: this.playerType, 
        playerState: [this.LFingers, this.RFingers],
        activeHand: hand
      };

      this.playerAction.emit( this.send );
  }
}
