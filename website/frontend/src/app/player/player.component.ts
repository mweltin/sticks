import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges, SimpleChange  } from '@angular/core';

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
  constructor() { }

  ngOnInit(): void {
    
  }

  swap() {
    this.swapAction.emit("perform swap action for " + this.playerType +"." );
  }

  handClickedHandler(hand: string) {
    
      this.playerAction.emit(
        { 
          'playerType': this.playerType, 
          'state': [this.LFingers, this.RFingers],
          'activeHand': hand
        }
      );
  }
}
