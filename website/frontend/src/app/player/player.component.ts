import { Component, OnInit, Input  } from '@angular/core';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit {

  @Input()
  playerType: string = '';

  constructor() { }

  ngOnInit(): void {
  }
  swap() {
    alert("perform swap action for " + this.playerType +"." );
  }

  handClickedHandler(hand: string) {
    console.log(this.playerType+"'s "+ hand + " has been clicked");
  }
}
