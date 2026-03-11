from ultralytics import YOLO
import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path="../config", config_name="default")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    model = YOLO(cfg.model.weights)

    model.train(
        data=cfg.data.yolo_data,
        epochs=cfg.trainer.epochs,
        batch=cfg.trainer.batch,
        imgsz=cfg.trainer.imgsz,
        device=cfg.trainer.device,
        workers=cfg.trainer.workers,
        patience=cfg.trainer.patience,
        optimizer=cfg.trainer.optimizer,
        lr0=cfg.trainer.lr0,
        lrf=cfg.trainer.lrf,
        weight_decay=cfg.trainer.weight_decay,
        project=cfg.trainer.project,
        name=cfg.trainer.name,
        pretrained=cfg.trainer.pretrained,
        save=cfg.trainer.save,
        plots=cfg.trainer.plots,
        exist_ok=cfg.trainer.exist_ok,
        verbose=cfg.trainer.verbose,
        resume=cfg.trainer.resume,
        multi_scale=cfg.trainer.multi_scale,
        deterministic=cfg.trainer.deterministic
    )


if __name__ == "__main__":
    main()