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
  
  constructor() { }

  ngOnInit(): void {
    
  }

  swap() {
    alert("perform swap action for " + this.playerType +"." );
  }

  handClickedHandler(hand: string) {
    
      this.playerAction.emit(
        { 
          'playerType': this.playerType, 
          'state': [this.LFingers, this.RFingers],
          'activeHand': hand
        }
      );
 

    // console.log(this.playerType+"'s "+ hand + " has been clicked");
    // if(hand == "right")
    // {
    //   this.RFingers = ++this.RFingers % 5;
    // }

    // if(hand == "left")
    // {
    //   this.LFingers = ++this.LFingers % 5;
    // }
    
  }
}
