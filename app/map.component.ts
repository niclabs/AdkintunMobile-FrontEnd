import { ActivatedRoute } from '@angular/router';
import { Component, OnInit} from '@angular/core';
import {
GOOGLE_MAPS_DIRECTIVES,
GOOGLE_MAPS_PROVIDERS
} from 'angular2-google-maps/core';

@Component({
  selector: 'my-map-detail',
  template: `
            <span> Mapa aca</span>
            `,
})
export class MapComponent implements OnInit{


  ngOnInit() {
  }
}