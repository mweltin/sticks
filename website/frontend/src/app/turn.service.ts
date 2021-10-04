import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { ActionQueue } from './action-queue';

@Injectable({
  providedIn: 'root'
})

export class TurnService {

  constructor(private http: HttpClient) { }

  private turnEndpoint = '/turn';

  takeATurn(turnData: ActionQueue){
    return this.http.post(this.turnEndpoint, {turnData});
  }
}



