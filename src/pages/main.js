import React, {Component} from 'react';
import {Container, Col, Row, Input, Table, Alert} from 'reactstrap';
import "./../css/main.css";
import { restElement } from '@babel/types';

class Main extends Component {
    constructor(props){
        super(props);
        this.state = {
            infractions: []
        };
    }

    async getInfractions(userId){
        await fetch("https://discord-security-api.herokuapp.com/infractionsDiscordId?id=" + userId)
        .then((res) => res.json())
        .then((resJson) => {
            console.log(resJson)
            this.setState({infractions: resJson})
        })
        .catch((error) => /*alert("Something went wrong! Please seek help at https://github.com/saulojoab/Discord-Security-Portal")*/ alert(error));
    }

    render(){
        return (
            <Container fluid>
                <Row className="menuContainer shadow">
                    <Col className="menuText">
                        Discord Security Portal
                    </Col>
                </Row>
                <Row>
                    <Col xs="12" className="searchText">
                        Insert user <b>Discord ID</b> below to see their infraction record:
                    </Col>
                    <Col sm="12" md={{ size: 6, offset: 3 }}>
                     <Input onChange={(evt) => this.getInfractions(evt.target.value)} className="searchBox" placeholder="EX: 396083444087652352"/>
                    </Col>
                </Row>
                {this.state.infractions.length == 0 ? (
                    <Row>
                        <Col className="userWarning">
                           <Alert>No users were found yet or the user has no infractions.</Alert>
                        </Col>
                    </Row>
                ) : (
                    <Row>
                    <Col>
                        <Table className="table" striped hover responsive bordered>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Description</th>
                                <th>Action Taken</th>
                            </tr>
                        </thead>
                        <tbody>
                        {this.state.infractions.map((i) => {
                            return(
                                <tr>
                                <th scope="row">{i.id}</th>
                                <td>{i.description}</td>
                                <td>{i.actionTaken == "infraction" ? "Only registered the infraction" : i.actionTaken}</td>
                            </tr>
                            )
                        })}
                            
                        </tbody>
                        </Table>
                    </Col>
                </Row>
                )}
            </Container>
        );
    }
}

export default Main;
