import { Component, OnInit } from '@angular/core';
import { TurnService } from "../turn.service";

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  history: string[] = [];

  constructor(private turnSrv: TurnService) { }

  ngOnInit(): void {
    this.turnSrv.currentPlay.subscribe(msg => this.history.push(msg) );
  }

}
