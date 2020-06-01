import React from 'react';

export default function Dog(props) {
    const genderLookup = {m: 'Male', f: 'Female'};
    const sizeLookup = {s: 'Small', m: 'Medium', l: 'Large', xl: 'Extra Large'};
    const reflexivePronouns = {m: 'himself', f: 'herself', u: 'itself'};

    const mediaUrl = 'http://127.0.0.1:8000/media/images/dogs/';
    const imageSrc = mediaUrl + props.details.image_filename;
    const name = props.details.name;
    const breed = props.details.breed;
    const age = props.details.age;
    const gender = genderLookup[props.details.gender];
    const size = sizeLookup[props.details.size];

    const catFood = props.details.favorite_cat_food;
    const frenchFilms = props.details.french_films;
    const chickenNoises = props.details.chicken_noises;
    const robot = Boolean(props.details.type === 'r');
    const carlSagan = props.details.is_carl_sagan;

    const rp = reflexivePronouns[props.details.gender];
    const info = [catFood, frenchFilms, chickenNoises, robot, carlSagan];
    const additionalInfo = info.some(item => !!item);

    return (
      <div>
        <h2 className='text-center dog-header'>{name}</h2>
        <img src={imageSrc} alt={name} />

        <p className="dog-card d-flex justify-space-around">
          <span>{breed}</span>
          <span>&bull;</span>
          <span>{age} Months</span>
          <span>&bull;</span>
          <span>{gender || 'Gender Unknown'}</span>
          <span>&bull;</span>
          <span>{size || 'Size Unknown'}</span>
        </p>

        {props.dogControls}

        {additionalInfo && <p className='bold'>Here are some amazing facts about {name} to help you make a decision!</p>}
          <div>
            {catFood && <p>{name}'s favorite brand of cat food is {catFood}!</p>}
            {frenchFilms && <p>{name} loves to watch classy French films!</p>}
            {chickenNoises && <p>{name} is a very sensitive individual who sometimes feels the need to
              express {rp} through interpretive dance and high-pitched chicken noises.</p>}
            {robot && <p>{name} is a robot! (And possibly a ninja. We didn't ask, but most robots are ninjas.)</p>}
            {carlSagan &&
              <p>
                This dog claims to be Carl Sagan.
                That's great! We don't think anyone would lie about something like that,
                so it's definitely true!
              </p>}
          </div>
      </div>
    );
  };
