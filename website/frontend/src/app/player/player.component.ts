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

  @Input()
  flip: Boolean = false;

  @Output() 
  playerActionAtr: EventEmitter<PlayerAction> = new EventEmitter();

  @Output() 
  swapAction: EventEmitter<any> = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
    
  }

  swap() {
    let hand = [this.LFingers, this.RFingers];
    hand.sort();
    let temp = hand[1] / 2; 
    this.swapAction.emit({'playerType':this.playerType, 'value':temp});
  }

  handClickedHandler(hand: string) {
      let send = { 
        playerType: this.playerType, 
        playerState: [this.LFingers, this.RFingers],
        activeHand: hand
      };

      this.playerActionAtr.emit( send );
  }

  canSwap(): Boolean {
    if( ( this.LFingers == 0 &&  ! (this.RFingers % 2)) || (this.RFingers == 0 && ! (this.LFingers % 2))){
        return true;
    }
    return false;
  }
}
