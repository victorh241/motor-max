-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema motormax
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema motormax
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `motormax` DEFAULT CHARACTER SET utf8 ;
USE `motormax` ;

-- -----------------------------------------------------
-- Table `motormax`.`Clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Clientes` (
  `id_cliente` INT NOT NULL AUTO_INCREMENT,
  `cpf` VARCHAR(14) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  PRIMARY KEY (`id_cliente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Veiculos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Veiculos` (
  `id_veiculo` INT NOT NULL AUTO_INCREMENT,
  `id_cliente` INT NOT NULL,
  `placa` VARCHAR(11) NOT NULL,
  `ano` YEAR NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_veiculo`),
  UNIQUE INDEX `placa_UNIQUE` (`placa` ASC) VISIBLE,
  INDEX `fk_Veiculo_Cliente1_idx` (`id_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_Veiculo_Cliente1`
    FOREIGN KEY (`id_cliente`)
    REFERENCES `motormax`.`Clientes` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Produtos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Produtos` (
  `id_produto` INT NOT NULL AUTO_INCREMENT,
  `codigo_produto` VARCHAR(7) NOT NULL,
  `descrição` VARCHAR(45) NOT NULL,
  `preco_unitario` DECIMAL(10,2) NOT NULL,
  `em_estoque` INT NOT NULL,
  PRIMARY KEY (`id_produto`),
  UNIQUE INDEX `codigo_peça_UNIQUE` (`codigo_produto` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Serviços`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Serviços` (
  `id_serviço` INT NOT NULL AUTO_INCREMENT,
  `id_produto` INT NULL,
  `descrição` VARCHAR(45) NOT NULL,
  `valorMaoObra` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_serviço`),
  INDEX `fk_Serviço_Produtos1_idx` (`id_produto` ASC) VISIBLE,
  CONSTRAINT `fk_Serviço_Produtos1`
    FOREIGN KEY (`id_produto`)
    REFERENCES `motormax`.`Produtos` (`id_produto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Funcionario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Funcionarios` (
  `id_funcionario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `CPF` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `disponivel` TINYINT NOT NULL,
  PRIMARY KEY (`id_funcionario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Atendente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Atendente` (
  `Clientes_id_cliente` INT NOT NULL,
  `Funcionario_id_funcionario` INT NOT NULL,
  PRIMARY KEY (`Clientes_id_cliente`, `Funcionario_id_funcionario`),
  INDEX `fk_Clientes_has_Funcionario_Funcionario1_idx` (`Funcionario_id_funcionario` ASC) VISIBLE,
  INDEX `fk_Clientes_has_Funcionario_Clientes1_idx` (`Clientes_id_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_Clientes_has_Funcionario_Clientes1`
    FOREIGN KEY (`Clientes_id_cliente`)
    REFERENCES `motormax`.`Clientes` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Clientes_has_Funcionario_Funcionario1`
    FOREIGN KEY (`Funcionario_id_funcionario`)
    REFERENCES `motormax`.`Funcionario` (`id_funcionario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Ordem de Serviço`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Ordem de Serviços` (
  `id_ordemServiço` INT NOT NULL AUTO_INCREMENT,
  `id_funcionario` INT NOT NULL,
  `id_cliente` INT NOT NULL,
  `id_serviço` INT NOT NULL,
  `codigo` VARCHAR(7) NOT NULL,
  `id_veiculo` INT NOT NULL,
  `Status` VARCHAR(30) NOT NULL,
  `desconto` DECIMAL(4,2) NULL,
  `Agendamento` VARCHAR(10) NOT NULL,
  `quantidade_produtos` INT NULL,
  `quantidade_serviços` INT NOT NULL,
  INDEX `fk_Serviço_Carro1_idx` (`id_veiculo` ASC) VISIBLE,
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) VISIBLE,
  PRIMARY KEY (`id_ordemServiço`),
  INDEX `fk_Ordem de Serviço_Serviço1_idx` (`id_serviço` ASC) VISIBLE,
  INDEX `fk_Ordem de Serviço_Atendente1_idx` (`id_cliente` ASC, `id_funcionario` ASC) VISIBLE,
  CONSTRAINT `fk_Serviço_Carro1`
    FOREIGN KEY (`id_veiculo`)
    REFERENCES `motormax`.`Veiculos` (`id_veiculo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ordem de Serviço_Serviço1`
    FOREIGN KEY (`id_serviço`)
    REFERENCES `motormax`.`Serviços` (`id_serviço`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ordem de Serviço_Atendente1`
    FOREIGN KEY (`id_cliente` , `id_funcionario`)
    REFERENCES `motormax`.`Atendente` (`Clientes_id_cliente` , `Funcionario_id_funcionario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`mecanicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`mecanicos` (
  `id_mecanico` INT NOT NULL AUTO_INCREMENT,
  `id_funcionario` INT NOT NULL,
  PRIMARY KEY (`id_mecanico`),
  INDEX `fk_mecanico_Funcionario1_idx` (`id_funcionario` ASC) VISIBLE,
  CONSTRAINT `fk_mecanico_Funcionario1`
    FOREIGN KEY (`id_funcionario`)
    REFERENCES `motormax`.`Funcionario` (`id_funcionario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Telefones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Telefones` (
  `id_telefone` INT NOT NULL AUTO_INCREMENT,
  `id_cliente` INT NOT NULL,
  `telefone` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id_telefone`),
  INDEX `fk_Telefone_Cliente1_idx` (`id_cliente` ASC) VISIBLE,
  CONSTRAINT `fk_Telefone_Cliente1`
    FOREIGN KEY (`id_cliente`)
    REFERENCES `motormax`.`Clientes` (`id_cliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`Usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `id_funcionario` INT NOT NULL,
  `login` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `função` ENUM("Atendente", "Mecânico", "admin") NOT NULL,
  PRIMARY KEY (`id_usuario`),
  INDEX `fk_Usuarios_Funcionario1_idx` (`id_funcionario` ASC) VISIBLE,
  CONSTRAINT `fk_Usuarios_Funcionario1`
    FOREIGN KEY (`id_funcionario`)
    REFERENCES `motormax`.`Funcionarios` (`id_funcionario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `motormax`.`equipe_mecanicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `motormax`.`equipe_mecanicos` (
  `mecanicos_id_mecanico` INT NOT NULL,
  `Ordem de Serviço_id_ordemServiço` INT NOT NULL,
  PRIMARY KEY (`mecanicos_id_mecanico`, `Ordem de Serviço_id_ordemServiço`),
  INDEX `fk_mecanicos_has_Ordem de Serviço_Ordem de Serviço1_idx` (`Ordem de Serviço_id_ordemServiço` ASC) VISIBLE,
  INDEX `fk_mecanicos_has_Ordem de Serviço_mecanicos1_idx` (`mecanicos_id_mecanico` ASC) VISIBLE,
  CONSTRAINT `fk_mecanicos_has_Ordem de Serviço_mecanicos1`
    FOREIGN KEY (`mecanicos_id_mecanico`)
    REFERENCES `motormax`.`mecanicos` (`id_mecanico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_mecanicos_has_Ordem de Serviço_Ordem de Serviço1`
    FOREIGN KEY (`Ordem de Serviço_id_ordemServiço`)
    REFERENCES `motormax`.`Ordem de Serviço` (`id_ordemServiço`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO funcionarios(nome, cpf, email, disponivel) VALUES ("joão", "1xx.xxx.xxx-xx", "lucas@gmail.com",1);
SELECT * FROM funcionarios;

INSERT INTO usuarios(id_funcionario, login, senha, função) VALUES (1 ,"admin", "123456", "admin");
SELECT * FROM usuarios;

SELECT * FROM produtos;
SELECT * FROM serviços;

SELECT * FROM veiculos;
SELECT * FROM clientes;

select * FROM `ordem de serviços`;