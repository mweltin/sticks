import { Component, OnInit } from '@angular/core';
import { TurnService } from "../turn.service";

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  history: string[] = [];
  buffer: string[] = [];

  constructor(private turnSrv: TurnService) { }

  ngOnInit(): void {
    this.turnSrv.currentPlay.subscribe(
      msg => {
        if (msg.length) {
          this.buffer.push(msg);
          this.history = this.buffer.slice().reverse()
        }
      }
    )
  }


}
